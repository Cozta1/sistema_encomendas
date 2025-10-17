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
        fields = ('username', 'nome_completo', 'cargo', 'identificacao', 'equipe')

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ['equipe']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FornecedorForm(forms.ModelForm):
    class Meta: model = Fornecedor; exclude = ['equipe']

class ProdutoForm(forms.ModelForm):
    class Meta: model = Produto; exclude = ['equipe']

class EncomendaForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        # Campos a serem preenchidos na criação/edição da encomenda
        fields = ['cliente', 'valor_pago_adiantamento', 'data_prevista_entrega', 'observacoes', 'status']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'valor_pago_adiantamento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'data_prevista_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}), # Para alterar o status na edição
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.is_authenticated and user.equipe:
            self.fields['cliente'].queryset = Cliente.objects.filter(equipe=user.equipe).order_by('nome')
        else:
            self.fields['cliente'].queryset = Cliente.objects.none()

class EntregaForm(forms.ModelForm):
    """Formulário apenas para os dados da execução da entrega."""
    class Meta:
        model = Entrega
        fields = ['responsavel_entrega', 'data_entrega_realizada', 'hora_entrega', 'entregue_por', 'assinatura_cliente']
        widgets = {
            'responsavel_entrega': forms.TextInput(attrs={'class': 'form-control'}),
            'data_entrega_realizada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_entrega': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'entregue_por': forms.TextInput(attrs={'class': 'form-control'}),
            'assinatura_cliente': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ItemEncomendaForm(forms.ModelForm):
    class Meta:
        model = ItemEncomenda
        fields = ['produto', 'fornecedor', 'quantidade', 'preco_cotado', 'observacoes']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control produto-select'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
            'preco_cotado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Preencha o valor'}),
            'observacoes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated and user.equipe:
            self.fields['produto'].queryset = Produto.objects.filter(equipe=user.equipe).order_by('nome')
            self.fields['fornecedor'].queryset = Fornecedor.objects.filter(equipe=user.equipe).order_by('nome')
        else:
            self.fields['produto'].queryset = Produto.objects.none()
            self.fields['fornecedor'].queryset = Fornecedor.objects.none()

ItemEncomendaFormSet = inlineformset_factory(Encomenda, ItemEncomenda, form=ItemEncomendaForm, extra=1, can_delete=True)