from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Equipe, Cliente, Fornecedor, Produto, 
    Encomenda, ItemEncomenda, Entrega
)
from .forms import CustomUserCreationForm, CustomUserChangeForm

# --- Administração de Autenticação e Equipe ---

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'nome_completo', 'cargo', 'equipe', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('nome_completo', 'cargo', 'identificacao', 'equipe')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('nome_completo', 'cargo', 'identificacao', 'equipe')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Equipe) # Registra o modelo Equipe no admin


# --- Administração dos Modelos da Aplicação ---

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'bairro', 'telefone', 'equipe']
    list_filter = ['equipe', 'bairro']
    search_fields = ['nome', 'cpf', 'rua', 'bairro']
    ordering = ['nome']

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'contato', 'telefone', 'equipe']
    list_filter = ['equipe']
    search_fields = ['nome', 'codigo', 'contato']
    ordering = ['nome']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'categoria', 'preco_base', 'equipe']
    list_filter = ['equipe', 'categoria']
    search_fields = ['nome', 'codigo']
    ordering = ['nome']


class ItemEncomendaInline(admin.TabularInline):
    model = ItemEncomenda
    extra = 1
    readonly_fields = ['valor_total']
    autocomplete_fields = ['produto', 'fornecedor']

class EntregaInline(admin.StackedInline):
    model = Entrega
    extra = 0

@admin.register(Encomenda)
class EncomendaAdmin(admin.ModelAdmin):
    list_display = ['numero_encomenda', 'cliente', 'status', 'data_encomenda', 'responsavel_criacao', 'valor_total']
    list_filter = ['status', 'equipe', 'data_encomenda']
    search_fields = ['numero_encomenda', 'cliente__nome']
    ordering = ['-data_encomenda']
    readonly_fields = ['numero_encomenda', 'valor_total']
    inlines = [ItemEncomendaInline, EntregaInline]
    autocomplete_fields = ['cliente']
    
    fieldsets = (
        ('Informações Principais', {
            'fields': ('numero_encomenda', 'equipe', 'cliente', 'status', 'responsavel_criacao')
        }),
        ('Valores e Prazos', {
            'fields': ('valor_total', 'valor_pago_adiantamento', 'data_prevista_entrega')
        }),
        ('Detalhes', {
            'fields': ('data_encomenda', 'observacoes')
        }),
    )