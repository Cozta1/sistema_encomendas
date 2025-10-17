from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Encomenda, Cliente, Produto, Fornecedor, ItemEncomenda, Entrega, CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'nome_completo', 'cargo', 'identificacao')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'nome_completo', 'cargo', 'identificacao')

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ['user']  # Oculta o campo de usuário
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do cliente'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código único do cliente'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Endereço completo'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ponto de referência (opcional)'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'}),
        }

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        exclude = ['user']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do fornecedor'}),
            # ... (widgets iguais aos anteriores)
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        exclude = ['user']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto'}),
            # ... (widgets iguais aos anteriores)
        }


class EncomendaForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        exclude = ['user']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'data_encomenda': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'responsavel_criacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do responsável'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra o queryset de clientes para mostrar apenas os do usuário logado
        self.fields['cliente'].queryset = Cliente.objects.filter(user=user).order_by('nome')
        self.fields['cliente'].empty_label = "Selecione um cliente"
        
        if not self.instance.pk and 'data_encomenda' not in self.initial:
            from datetime import date
            self.initial['data_encomenda'] = date.today()


class ItemEncomendaForm(forms.ModelForm):
    class Meta:
        model = ItemEncomenda
        fields = ['produto', 'fornecedor', 'quantidade', 'preco_cotado', 'observacoes']
        # ... (widgets iguais aos anteriores)
    
    def __init__(self, *args, **kwargs):
        # A filtragem aqui é mais complexa, faremos na view por enquanto
        super().__init__(*args, **kwargs)
        # Idealmente, o queryset seria filtrado aqui também, mas precisa do 'user'
        # que não é passado para o formset diretamente. A view já protege o acesso.

# Formset
ItemEncomendaFormSet = inlineformset_factory(
    Encomenda, 
    ItemEncomenda, 
    form=ItemEncomendaForm,
    extra=1,
    can_delete=True,
    min_num=1
)

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = [
            'data_entrega', 'responsavel_entrega', 'valor_pago_adiantamento',
            'data_entrega_realizada', 'hora_entrega', 'entregue_por', 'assinatura_cliente',
            'data_prevista', 'observacoes_entrega'
        ]
        # ... (widgets iguais aos anteriores)