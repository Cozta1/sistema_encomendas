from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Importações dos modelos e formulários
from .models import Encomenda, Cliente, Produto, Fornecedor, ItemEncomenda, Entrega
from .forms import (
    EncomendaForm, ItemEncomendaFormSet, EntregaForm, ClienteForm, 
    ProdutoForm, FornecedorForm, CustomUserCreationForm
)

# --- Autenticação ---
def register(request):
    """View de Cadastro de Usuário com o formulário personalizado."""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta para "{username}" criada com sucesso! Você já pode fazer o login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'encomendas/register.html', {'form': form})


# --- Views Principais (Protegidas por Login) ---
@login_required
def dashboard(request):
    """Dashboard principal com estatísticas."""
    total_encomendas = Encomenda.objects.count()
    encomendas_pendentes = Encomenda.objects.filter(status__in=['criada', 'cotacao', 'aprovada', 'em_andamento']).count()
    encomendas_entregues = Encomenda.objects.filter(status='entregue').count()
    
    ultimas_encomendas = Encomenda.objects.select_related('cliente').order_by('-data_criacao')[:5]
    
    context = {
        'total_encomendas': total_encomendas,
        'encomendas_pendentes': encomendas_pendentes,
        'encomendas_entregues': encomendas_entregues,
        'ultimas_encomendas': ultimas_encomendas,
    }
    return render(request, 'encomendas/dashboard.html', context)

@login_required
def encomenda_list(request):
    """Lista todas as encomendas com filtros."""
    encomendas = Encomenda.objects.select_related('cliente').prefetch_related('entrega').order_by('-numero_encomenda')
    
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
            Q(cliente__codigo__icontains=search) |
            Q(itens__produto__nome__icontains=search) |
            Q(itens__produto__codigo__icontains=search)
        ).distinct()
    
    paginator = Paginator(encomendas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    clientes = Cliente.objects.all().order_by('nome')
    status_choices = Encomenda.STATUS_CHOICES
    
    context = {
        'page_obj': page_obj,
        'clientes': clientes,
        'status_choices': status_choices,
        'current_status': status_filter,
        'current_cliente': int(cliente_filter) if cliente_filter else None,
        'current_search': search,
    }
    return render(request, 'encomendas/encomenda_list.html', context)

@login_required
def encomenda_detail(request, pk):
    """Detalhes de uma encomenda específica."""
    encomenda = get_object_or_404(Encomenda, pk=pk)
    itens = encomenda.itens.select_related('produto', 'fornecedor').all()
    
    try:
        entrega = encomenda.entrega
    except Entrega.DoesNotExist:
        entrega = None
    
    context = {
        'encomenda': encomenda,
        'itens': itens,
        'entrega': entrega,
    }
    return render(request, 'encomendas/encomenda_detail.html', context)

@login_required
def encomenda_create(request):
    """Criar nova encomenda."""
    if request.method == 'POST':
        form = EncomendaForm(request.POST)
        formset = ItemEncomendaFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            encomenda = form.save()
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE', False):
                    item = item_form.save(commit=False)
                    item.encomenda = encomenda
                    item.save()
            
            encomenda.calcular_valor_total()
            
            messages.success(request, f'Encomenda #{encomenda.numero_encomenda} criada com sucesso!')
            return redirect('encomenda_detail', pk=encomenda.pk)
    else:
        form = EncomendaForm()
        formset = ItemEncomendaFormSet()
    
    context = {'form': form, 'formset': formset, 'title': 'Nova Encomenda'}
    return render(request, 'encomendas/encomenda_form.html', context)

@login_required
def encomenda_edit(request, pk):
    """Editar encomenda existente."""
    encomenda = get_object_or_404(Encomenda, pk=pk)
    
    if request.method == 'POST':
        form = EncomendaForm(request.POST, instance=encomenda)
        formset = ItemEncomendaFormSet(request.POST, instance=encomenda)
        
        if form.is_valid() and formset.is_valid():
            encomenda = form.save()
            formset.save()
            encomenda.calcular_valor_total()
            messages.success(request, f'Encomenda #{encomenda.numero_encomenda} atualizada com sucesso!')
            return redirect('encomenda_detail', pk=encomenda.pk)
    else:
        form = EncomendaForm(instance=encomenda)
        formset = ItemEncomendaFormSet(instance=encomenda)
    
    context = {
        'form': form,
        'formset': formset,
        'encomenda': encomenda,
        'title': f'Editar Encomenda #{encomenda.numero_encomenda}',
    }
    return render(request, 'encomendas/encomenda_form.html', context)

@login_required
def encomenda_delete(request, pk):
    encomenda = get_object_or_404(Encomenda, pk=pk)
    if request.method == 'POST':
        numero = encomenda.numero_encomenda
        encomenda.delete()
        messages.success(request, f'Encomenda #{numero} excluída com sucesso!')
        return redirect('encomenda_list')
    context = {'encomenda': encomenda}
    return render(request, 'encomendas/encomenda_confirm_delete.html', context)

@login_required
def entrega_create(request, encomenda_pk):
    encomenda = get_object_or_404(Encomenda, pk=encomenda_pk)
    try:
        entrega = encomenda.entrega
        return redirect('entrega_edit', pk=entrega.pk)
    except Entrega.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = EntregaForm(request.POST)
        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.encomenda = encomenda
            entrega.save()
            messages.success(request, 'Informações de entrega criadas com sucesso!')
            return redirect('encomenda_detail', pk=encomenda.pk)
    else:
        form = EntregaForm()
    
    context = {
        'form': form,
        'encomenda': encomenda,
        'title': f'Programar Entrega - Encomenda #{encomenda.numero_encomenda}',
    }
    return render(request, 'encomendas/entrega_form.html', context)

@login_required
def entrega_edit(request, pk):
    entrega = get_object_or_404(Entrega, pk=pk)
    if request.method == 'POST':
        form = EntregaForm(request.POST, instance=entrega)
        if form.is_valid():
            entrega = form.save()
            if entrega.data_entrega_realizada and entrega.assinatura_cliente:
                entrega.encomenda.status = 'entregue'
                entrega.encomenda.save()
            messages.success(request, 'Informações de entrega atualizadas com sucesso!')
            return redirect('encomenda_detail', pk=entrega.encomenda.pk)
    else:
        form = EntregaForm(instance=entrega)
    
    context = {
        'form': form,
        'entrega': entrega,
        'title': f'Editar Entrega - Encomenda #{entrega.encomenda.numero_encomenda}',
    }
    return render(request, 'encomendas/entrega_form.html', context)

@login_required
def cliente_list(request):
    clientes = Cliente.objects.all().order_by('nome')
    search = request.GET.get('search')
    if search:
        clientes = clientes.filter(Q(nome__icontains=search) | Q(codigo__icontains=search) | Q(endereco__icontains=search))
    paginator = Paginator(clientes, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {'page_obj': page_obj, 'current_search': search}
    return render(request, 'encomendas/cliente_list.html', context)

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente {cliente.nome} criado com sucesso!')
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    context = {'form': form, 'title': 'Novo Cliente'}
    return render(request, 'encomendas/cliente_form.html', context)

@login_required
def produto_list(request):
    produtos = Produto.objects.all().order_by('nome')
    search = request.GET.get('search')
    if search:
        produtos = produtos.filter(Q(nome__icontains=search) | Q(codigo__icontains=search) | Q(categoria__icontains=search))
    paginator = Paginator(produtos, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {'page_obj': page_obj, 'current_search': search}
    return render(request, 'encomendas/produto_list.html', context)

@login_required
def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save()
            messages.success(request, f'Produto {produto.nome} criado com sucesso!')
            return redirect('produto_list')
    else:
        form = ProdutoForm()
    context = {'form': form, 'title': 'Novo Produto'}
    return render(request, 'encomendas/produto_form.html', context)

@login_required
def fornecedor_list(request):
    fornecedores = Fornecedor.objects.all().order_by('nome')
    search = request.GET.get('search')
    if search:
        fornecedores = fornecedores.filter(Q(nome__icontains=search) | Q(codigo__icontains=search) | Q(contato__icontains=search))
    paginator = Paginator(fornecedores, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {'page_obj': page_obj, 'current_search': search}
    return render(request, 'encomendas/fornecedor_list.html', context)

@login_required
def fornecedor_create(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            fornecedor = form.save()
            messages.success(request, f'Fornecedor {fornecedor.nome} criado com sucesso!')
            return redirect('fornecedor_list')
    else:
        form = FornecedorForm()
    context = {'form': form, 'title': 'Novo Fornecedor'}
    return render(request, 'encomendas/fornecedor_form.html', context)


# --- API (também protegida) ---
@login_required
@require_http_methods(["GET"])
def api_produto_info(request, produto_id):
    try:
        produto = Produto.objects.get(id=produto_id)
        data = {'nome': produto.nome, 'codigo': produto.codigo, 'preco_base': str(produto.preco_base)}
        return JsonResponse(data)
    except Produto.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)

@login_required
@require_http_methods(["POST"])
def api_update_status(request, encomenda_pk):
    encomenda = get_object_or_404(Encomenda, pk=encomenda_pk)
    new_status = request.POST.get('status')
    if new_status in dict(Encomenda.STATUS_CHOICES):
        encomenda.status = new_status
        encomenda.save()
        return JsonResponse({'success': True, 'status': encomenda.get_status_display()})
    return JsonResponse({'error': 'Status inválido'}, status=400)