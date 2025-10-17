from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from django.conf import settings

# --- Modelos de Autenticação e Equipe ---
class Equipe(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text="Nome da empresa ou equipe (ex: Drogaria Benfica - Centro)")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.nome

class CustomUser(AbstractUser):
    nome_completo = models.CharField(max_length=255, blank=True, verbose_name="Nome Completo")
    cargo = models.CharField(max_length=100, blank=True, verbose_name="Cargo")
    identificacao = models.CharField(max_length=100, blank=True, verbose_name="Identificação")
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True, blank=True, related_name="membros")
    def __str__(self): return self.username

# --- Modelos Principais da Aplicação ---
class Cliente(models.Model):
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name="clientes")
    nome = models.CharField(max_length=200, verbose_name="Nome do Cliente")
    cpf = models.CharField(max_length=14, blank=True, verbose_name="CPF")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    
    # Endereço completo (com campos opcionais)
    rua = models.CharField(max_length=255, blank=True, verbose_name="Rua / Logradouro")
    numero = models.CharField(max_length=20, blank=True, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, blank=True, verbose_name="Bairro")
    referencia = models.CharField(max_length=200, blank=True, verbose_name="Ponto de Referência")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name="fornecedores")
    nome = models.CharField(max_length=200, verbose_name="Nome do Fornecedor")
    codigo = models.CharField(max_length=50, verbose_name="Código")
    contato = models.CharField(max_length=200, blank=True, verbose_name="Contato")
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('equipe', 'codigo')
    def __str__(self): return self.nome

class Produto(models.Model):
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name="produtos")
    nome = models.CharField(max_length=200, verbose_name="Nome do Produto")
    codigo = models.CharField(max_length=50, verbose_name="Código")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    preco_base = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Preço Base")
    categoria = models.CharField(max_length=100, blank=True, verbose_name="Categoria")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('equipe', 'codigo')
    def __str__(self): return self.nome

class Encomenda(models.Model):
    STATUS_CHOICES = [
        ('criada', 'Criada'), ('cotacao', 'Em Cotação'), ('aprovada', 'Aprovada'),
        ('em_andamento', 'Em Andamento'), ('pronta', 'Pronta para Entrega'), ('entregue', 'Entregue'),
        ('cancelada', 'Cancelada'),
    ]

    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name="encomendas")
    numero_encomenda = models.AutoField(primary_key=True, verbose_name="Número da Encomenda")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    responsavel_criacao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Responsável pelo Pedido")
    data_encomenda = models.DateTimeField(default=timezone.now, verbose_name="Data do Pedido")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='criada', verbose_name="Status")
    valor_pago_adiantamento = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Valor de Adiantamento")
    data_prevista_entrega = models.DateField(null=True, blank=True, verbose_name="Data Prevista para Entrega")
    observacoes = models.TextField(blank=True, verbose_name="Observações Gerais")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Valor Total dos Itens")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: ordering = ['-numero_encomenda']
    def __str__(self): return f"Encomenda #{self.numero_encomenda} - {self.cliente.nome}"
    def calcular_valor_total(self):
        self.valor_total = sum(item.valor_total for item in self.itens.all()) if self.itens.exists() else Decimal('0.00')
        self.save()

class ItemEncomenda(models.Model):
    encomenda = models.ForeignKey(Encomenda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, verbose_name="Fornecedor")
    quantidade = models.PositiveIntegerField(default=1, verbose_name="Quantidade")
    preco_cotado = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name="Preço Cotado")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Valor Total")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.preco_cotado
        super().save(*args, **kwargs)
    def __str__(self): return f"{self.produto.nome} - Qtd: {self.quantidade}"

class Entrega(models.Model):
    encomenda = models.OneToOneField(Encomenda, on_delete=models.CASCADE, verbose_name="Encomenda")
    responsavel_entrega = models.CharField(max_length=100, blank=True, verbose_name="Responsável pela Entrega")
    data_entrega_realizada = models.DateField(null=True, blank=True, verbose_name="Data da Entrega")
    hora_entrega = models.TimeField(null=True, blank=True, verbose_name="Hora da Entrega")
    entregue_por = models.CharField(max_length=100, blank=True, verbose_name="Entregue por")
    assinatura_cliente = models.TextField(blank=True, verbose_name="Assinatura/Recebedor")
    def __str__(self): return f"Entrega da Encomenda #{self.encomenda.numero_encomenda}"