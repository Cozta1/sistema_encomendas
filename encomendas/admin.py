from django.contrib import admin
from .models import Cliente, Fornecedor, Produto, Encomenda, ItemEncomenda, Entrega


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'bairro', 'telefone']
    list_filter = ['bairro', 'created_at']
    search_fields = ['nome', 'codigo', 'endereco']
    ordering = ['nome']


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'telefone', 'email']
    list_filter = ['created_at']
    search_fields = ['nome', 'codigo', 'contato']
    ordering = ['nome']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'categoria', 'preco_base']
    list_filter = ['categoria', 'created_at']
    search_fields = ['nome', 'codigo', 'descricao']
    ordering = ['nome']


class ItemEncomendaInline(admin.TabularInline):
    model = ItemEncomenda
    extra = 1
    fields = ['produto', 'fornecedor', 'quantidade', 'preco_cotado', 'valor_total', 'observacoes']
    readonly_fields = ['valor_total']


class EntregaInline(admin.StackedInline):
    model = Entrega
    extra = 0
    fields = [
        'data_entrega', 'responsavel_entrega', 'valor_pago_adiantamento',
        'data_entrega_realizada', 'hora_entrega', 'entregue_por', 
        'assinatura_cliente', 'observacoes_entrega'
    ]


@admin.register(Encomenda)
class EncomendaAdmin(admin.ModelAdmin):
    list_display = ['numero_encomenda', 'cliente', 'status', 'valor_total', 'data_criacao', 'responsavel_criacao']
    list_filter = ['status', 'data_criacao', 'responsavel_criacao']
    search_fields = ['numero_encomenda', 'cliente__nome', 'cliente__codigo']
    ordering = ['-numero_encomenda']
    readonly_fields = ['numero_encomenda', 'data_criacao', 'valor_total']
    inlines = [ItemEncomendaInline, EntregaInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('numero_encomenda', 'cliente', 'data_encomenda', 'data_criacao', 'responsavel_criacao')
        }),
        ('Status e Valores', {
            'fields': ('status', 'valor_total', 'observacoes')
        }),
    )


@admin.register(ItemEncomenda)
class ItemEncomendaAdmin(admin.ModelAdmin):
    list_display = ['encomenda', 'produto', 'fornecedor', 'quantidade', 'preco_cotado', 'valor_total']
    list_filter = ['encomenda__status', 'produto__categoria']
    search_fields = ['encomenda__numero_encomenda', 'produto__nome', 'fornecedor__nome']
    readonly_fields = ['valor_total']


@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ['encomenda', 'data_entrega', 'responsavel_entrega', 'valor_pago_adiantamento', 'data_entrega_realizada']
    list_filter = ['data_entrega', 'data_entrega_realizada', 'responsavel_entrega']
    search_fields = ['encomenda__numero_encomenda', 'responsavel_entrega', 'entregue_por']
    readonly_fields = ['valor_restante']
    
    fieldsets = (
        ('Informações da Encomenda', {
            'fields': ('encomenda',)
        }),
        ('Dados do Formulário Físico', {
            'fields': ('data_entrega', 'responsavel_entrega', 'valor_pago_adiantamento')
        }),
        ('Execução da Entrega', {
            'fields': ('data_entrega_realizada', 'hora_entrega', 'entregue_por', 'assinatura_cliente')
        }),
        ('Controle Interno', {
            'fields': ('data_prevista', 'data_realizada', 'valor_restante', 'observacoes_entrega')
        }),
    )
