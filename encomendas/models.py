from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal

class CustomUser(AbstractUser):
    nome_completo = models.CharField(max_length=255, blank=True, verbose_name="Nome Completo")
    cargo = models.CharField(max_length=100, blank=True, verbose_name="Cargo")
    identificacao = models.CharField(max_length=100, blank=True, verbose_name="Identificação")

    def __str__(self):
        return self.username

class Cliente(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Cliente")
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código")
    endereco = models.TextField(verbose_name="Endereço")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    referencia = models.CharField(max_length=200, blank=True, verbose_name="Referência")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Fornecedor(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Fornecedor")
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código")
    contato = models.CharField(max_length=200, blank=True, verbose_name="Contato")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Produto(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Produto")
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    preco_base = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Preço Base"
    )
    categoria = models.CharField(max_length=100, blank=True, verbose_name="Categoria")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Encomenda(models.Model):
    STATUS_CHOICES = [
        ('criada', 'Criada'),
        ('cotacao', 'Em Cotação'),
        ('aprovada', 'Aprovada'),
        ('em_andamento', 'Em Andamento'),
        ('pronta', 'Pronta para Entrega'),
        ('entregue', 'Entregue'),
        ('cancelada', 'Cancelada'),
    ]

    numero_encomenda = models.AutoField(primary_key=True, verbose_name="Número da Encomenda")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação (sistema)")
    data_encomenda = models.DateField(verbose_name="Data", help_text="Data da encomenda (campo do cabeçalho)", default=timezone.now)
    responsavel_criacao = models.CharField(max_length=100, verbose_name="Responsável", 
                                         help_text="Responsável pela criação da encomenda")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='criada', verbose_name="Status")
    observacoes = models.TextField(blank=True, verbose_name="Observação", 
                                 help_text="Campo 'Observação' do formulário físico")
    
    valor_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        verbose_name="Valor do Produto",
        help_text="Valor total dos produtos da encomenda"
    )
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Encomenda"
        verbose_name_plural = "Encomendas"
        ordering = ['-numero_encomenda']

    def __str__(self):
        return f"Encomenda {self.numero_encomenda} - {self.cliente.nome}"

    def calcular_valor_total(self):
        total = sum(item.valor_total for item in self.itens.all())
        self.valor_total = total
        self.save()
        return total


class ItemEncomenda(models.Model):
    encomenda = models.ForeignKey(Encomenda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, verbose_name="Fornecedor")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    preco_cotado = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Preço Cotado"
    )
    valor_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Valor Total"
    )
    observacoes = models.TextField(blank=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Item da Encomenda"
        verbose_name_plural = "Itens da Encomenda"

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.preco_cotado
        super().save(*args, **kwargs)
        self.encomenda.calcular_valor_total()

    def __str__(self):
        return f"{self.produto.nome} - Qtd: {self.quantidade}"


class Entrega(models.Model):
    encomenda = models.OneToOneField(Encomenda, on_delete=models.CASCADE, verbose_name="Encomenda")
    
    data_entrega = models.DateField(verbose_name="Data Entrega", 
                                  help_text="Campo 'Data Entrega' do formulário físico",
                                  default=timezone.now)
    responsavel_entrega = models.CharField(max_length=100, verbose_name="Responsável Entrega",
                                         help_text="Campo 'Responsável Entrega' do formulário físico",
                                         default="A definir")
    
    valor_pago_adiantamento = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Valor Pago Adiantamento",
        help_text="Campo 'Valor Pago Adiantamento' do formulário físico"
    )
    
    data_entrega_realizada = models.DateField(null=True, blank=True, verbose_name="Data",
                                            help_text="Data da entrega realizada (seção inferior)")
    hora_entrega = models.TimeField(null=True, blank=True, verbose_name="Hora",
                                  help_text="Hora da entrega (seção inferior)")
    entregue_por = models.CharField(max_length=100, blank=True, verbose_name="Entregue por",
                                  help_text="Campo 'Entregue por' da seção inferior")
    
    assinatura_cliente = models.TextField(blank=True, verbose_name="Ass. do Cliente",
                                        help_text="Campo para assinatura do cliente")
    
    data_prevista = models.DateField(null=True, blank=True, verbose_name="Data Prevista (controle)")
    data_realizada = models.DateTimeField(null=True, blank=True, verbose_name="Data/Hora Realizada (controle)")
    observacoes_entrega = models.TextField(blank=True, verbose_name="Observações da Entrega")

    class Meta:
        verbose_name = "Entrega"
        verbose_name_plural = "Entregas"

    def __str__(self):
        return f"Entrega - Encomenda {self.encomenda.numero_encomenda}"

    @property
    def valor_restante(self):
        return self.encomenda.valor_total - self.valor_pago_adiantamento
    
    @property
    def valor_adiantamento(self):
        return self.valor_pago_adiantamento