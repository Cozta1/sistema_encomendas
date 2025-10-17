from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Encomenda, Cliente, Produto, Fornecedor, ItemEncomenda, Entrega, Equipe
from .forms import (
    EncomendaForm, ItemEncomendaFormSet, EntregaForm, ClienteForm,
    ProdutoForm, FornecedorForm, CustomUserCreationForm
)

# --- Autenticação e Gestão de Equipe ---

def register(request):
    """Página de registro para um novo usuário que também cria uma nova equipe."""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Cria a equipe primeiro
            nome_equipe = f"Equipe de {form.cleaned_data.get('username')}"
            equipe = Equipe.objects.create(nome=nome_equipe)
            
            # Cria o usuário e o associa à nova equipe
            user = form.save(commit=False)
            user.equipe = equipe
            user.save()
            
            messages.success(request, f'Conta e equipe "{nome_equipe}" criadas com sucesso! Você já pode fazer o login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'encomendas/register.html', {'form': form, 'title': 'Criar a Sua Equipe'})


# --- Views Principais (Filtradas por Equipe) ---

@login_required
def dashboard(request):
    """Dashboard principal com estatísticas da equipe."""
    equipe = request.user.equipe
    if not equipe:
        return render(request, 'encomendas/dashboard_sem_equipe.html')

    encomendas = Encomenda.objects.filter(equipe=equipe)
    context = {
        'total_encomendas': encomendas.count(),
        'encomendas_pendentes': encomendas.exclude(status__in=['entregue', 'cancelada']).count(),
        'encomendas_entregues': encomendas.filter(status='entregue').count(),
        'ultimas_encomendas': encomendas.select_related('cliente').order_by('-data_encomenda')[:5],
    }
    return render(request, 'encomendas/dashboard.html', context)

# --- CRUD de Encomendas ---

@login_required
def encomenda_list(request):
    """Lista todas as encomendas da equipe."""
    encomendas = Encomenda.objects.filter(equipe=request.user.equipe).select_related('cliente', 'responsavel_criacao').order_by('-numero_encomenda')
    
    status_filter = request.GET.get('status')
    cliente_filter = request.GET.get('cliente')
    search = request.GET.get('search')
    
    if status_filter:
        encomendas = encomendas.filter(status=status_filter)
    if cliente_filter:
        encomendas = encomendas.filter(cliente__id=cliente_filter)
    if search:
        encomendas = encomendas.filter(
            Q(numero_encomenda__icontains=search) |
            Q(cliente__nome__icontains=search) |
            Q(itens__produto__nome__icontains=search)
        ).distinct()

    paginator = Paginator(encomendas, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    context = {
        'page_obj': page_obj,
        'clientes': Cliente.objects.filter(equipe=request.user.equipe),
        'status_choices': Encomenda.STATUS_CHOICES,
        'current_status': status_filter,
        'current_cliente': int(cliente_filter) if cliente_filter else None,
        'current_search': search,
    }
    return render(request, 'encomendas/encomenda_list.html', context)

@login_required
def encomenda_detail(request, pk):
    encomenda = get_object_or_404(Encomenda, pk=pk, equipe=request.user.equipe)
    itens = encomenda.itens.select_related('produto', 'fornecedor').all()
    try:
        entrega = encomenda.entrega
    except Entrega.DoesNotExist:
        entrega = None
    
    context = {'encomenda': encomenda, 'itens': itens, 'entrega': entrega}
    return render(request, 'encomendas/encomenda_detail.html', context)

@login_required
def encomenda_create(request):
    if request.method == 'POST':
        form = EncomendaForm(request.user, request.POST)
        formset = ItemEncomendaFormSet(request.POST, form_kwargs={'user': request.user})
        
        if form.is_valid() and formset.is_valid():
            encomenda = form.save(commit=False)
            encomenda.equipe = request.user.equipe
            encomenda.responsavel_criacao = request.user
            encomenda.status = 'criada'
            encomenda.save()
            
            formset.instance = encomenda
            formset.save()
            
            encomenda.calcular_valor_total()
            messages.success(request, f'Encomenda #{encomenda.numero_encomenda} criada com sucesso!')
            return redirect('encomenda_detail', pk=encomenda.pk)
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = EncomendaForm(user=request.user)
        if 'status' in form.fields:
            form.fields.pop('status')
        formset = ItemEncomendaFormSet(form_kwargs={'user': request.user})
    
    return render(request, 'encomendas/encomenda_form.html', {'form': form, 'formset': formset, 'title': 'Nova Encomenda'})

@login_required
def encomenda_edit(request, pk):
    encomenda = get_object_or_404(Encomenda, pk=pk, equipe=request.user.equipe)
    entrega, created = Entrega.objects.get_or_create(encomenda=encomenda)

    if request.method == 'POST':
        form = EncomendaForm(request.user, request.POST, instance=encomenda)
        entrega_form = EntregaForm(request.POST, instance=entrega)
        formset = ItemEncomendaFormSet(request.POST, instance=encomenda, form_kwargs={'user': request.user})
        
        if form.is_valid() and formset.is_valid() and entrega_form.is_valid():
            form.save()
            entrega_form.save()
            formset.save()
            
            encomenda.calcular_valor_total()
            messages.success(request, f'Encomenda #{encomenda.numero_encomenda} atualizada com sucesso!')
            return redirect('encomenda_detail', pk=encomenda.pk)
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = EncomendaForm(user=request.user, instance=encomenda)
        entrega_form = EntregaForm(instance=entrega)
        formset = ItemEncomendaFormSet(instance=encomenda, form_kwargs={'user': request.user})
    
    context = {
        'form': form, 
        'formset': formset, 
        'entrega_form': entrega_form,
        'encomenda': encomenda,
        'title': f'Editar Encomenda #{encomenda.numero_encomenda}'
    }
    return render(request, 'encomendas/encomenda_form.html', context)

@login_required
def encomenda_delete(request, pk):
    encomenda = get_object_or_404(Encomenda, pk=pk, equipe=request.user.equipe)
    if request.method == 'POST':
        numero = encomenda.numero_encomenda
        encomenda.delete()
        messages.success(request, f'Encomenda #{numero} excluída com sucesso!')
        return redirect('encomenda_list')
    return render(request, 'encomendas/encomenda_confirm_delete.html', {'encomenda': encomenda})

# --- CRUD de Clientes, Produtos, Fornecedores ---

@login_required
def cliente_list(request):
    clientes = Cliente.objects.filter(equipe=request.user.equipe).order_by('nome')
    paginator = Paginator(clientes, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'encomendas/cliente_list.html', {'page_obj': page_obj})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.equipe = request.user.equipe
            cliente.save()
            messages.success(request, f'Cliente {cliente.nome} criado com sucesso!')
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'encomendas/cliente_form.html', {'form': form, 'title': 'Novo Cliente'})

@login_required
def produto_list(request):
    produtos = Produto.objects.filter(equipe=request.user.equipe).order_by('nome')
    paginator = Paginator(produtos, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'encomendas/produto_list.html', {'page_obj': page_obj})

@login_required
def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.equipe = request.user.equipe
            produto.save()
            messages.success(request, f'Produto {produto.nome} criado com sucesso!')
            return redirect('produto_list')
    else:
        form = ProdutoForm()
    return render(request, 'encomendas/produto_form.html', {'form': form, 'title': 'Novo Produto'})

@login_required
def fornecedor_list(request):
    fornecedores = Fornecedor.objects.filter(equipe=request.user.equipe).order_by('nome')
    paginator = Paginator(fornecedores, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'encomendas/fornecedor_list.html', {'page_obj': page_obj})

@login_required
def fornecedor_create(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            fornecedor = form.save(commit=False)
            fornecedor.equipe = request.user.equipe
            fornecedor.save()
            messages.success(request, f'Fornecedor {fornecedor.nome} criado com sucesso!')
            return redirect('fornecedor_list')
    else:
        form = FornecedorForm()
    return render(request, 'encomendas/fornecedor_form.html', {'form': form, 'title': 'Novo Fornecedor'})


# --- Endpoints da API (Protegidos) ---

@login_required
@require_http_methods(["POST"])
def api_update_status(request, encomenda_pk):
    encomenda = get_object_or_404(Encomenda, pk=encomenda_pk, equipe=request.user.equipe)
    new_status = request.POST.get('status')
    if new_status in dict(Encomenda.STATUS_CHOICES):
        encomenda.status = new_status
        encomenda.save()
        return JsonResponse({'success': True, 'status': encomenda.get_status_display()})
    return JsonResponse({'error': 'Status inválido'}, status=400)

@login_required
@require_http_methods(["GET"])
def api_produto_info(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, equipe=request.user.equipe)
    data = {'nome': produto.nome, 'codigo': produto.codigo, 'preco_base': str(produto.preco_base)}
    return JsonResponse(data)