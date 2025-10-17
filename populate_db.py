#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo, incluindo usuários personalizados.
"""
import os
import django
from decimal import Decimal
from datetime import date, datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_encomendas.settings')
django.setup()

from django.contrib.auth import get_user_model
from encomendas.models import Cliente, Fornecedor, Produto, Encomenda, ItemEncomenda, Entrega

# Obter o modelo de usuário personalizado
CustomUser = get_user_model()

def criar_dados_exemplo():
    print("--- Limpando dados antigos ---")
    # Limpa os modelos para evitar duplicação a cada execução
    ItemEncomenda.objects.all().delete()
    Entrega.objects.all().delete()
    Encomenda.objects.all().delete()
    Produto.objects.all().delete()
    Fornecedor.objects.all().delete()
    Cliente.objects.all().delete()
    CustomUser.objects.filter(is_superuser=False).delete() # Deleta usuários não-admin
    
    print("\n--- Criando dados de exemplo ---")

    # Criar Usuários
    users_data = [
        {
            'username': 'joao.farma',
            'password': 'Password123',
            'nome_completo': 'João da Silva',
            'cargo': 'Farmacêutico',
            'identificacao': 'CRF-MG 12345'
        },
        {
            'username': 'maria.atendente',
            'password': 'Password123',
            'nome_completo': 'Maria Oliveira',
            'cargo': 'Atendente',
            'identificacao': 'ATD-001'
        },
        {
            'username': 'carlos.caixa',
            'password': 'Password123',
            'nome_completo': 'Carlos Pereira',
            'cargo': 'Operador de Caixa',
            'identificacao': 'CX-002'
        },
    ]

    users = []
    for data in users_data:
        try:
            user = CustomUser.objects.create_user(
                username=data['username'],
                password=data['password'],
                nome_completo=data['nome_completo'],
                cargo=data['cargo'],
                identificacao=data['identificacao']
            )
            users.append(user)
            print(f"Usuário criado: {user.username}")
        except Exception as e:
            print(f"Usuário {data['username']} já existe ou ocorreu um erro: {e}")

    # Criar clientes
    clientes_data = [
        {'nome': 'Maria Silva Santos', 'codigo': 'CLI001', 'endereco': 'Rua das Flores, 123, Apt 201', 'bairro': 'Centro', 'referencia': 'Próximo ao Banco do Brasil', 'telefone': '(32) 99999-1234'},
        {'nome': 'João Carlos Oliveira', 'codigo': 'CLI002', 'endereco': 'Av. Presidente Vargas, 456', 'bairro': 'São Mateus', 'referencia': 'Em frente à padaria', 'telefone': '(32) 98888-5678'},
        {'nome': 'Ana Paula Costa', 'codigo': 'CLI003', 'endereco': 'Rua São João, 789', 'bairro': 'Benfica', 'referencia': 'Casa azul com portão branco', 'telefone': '(32) 97777-9012'},
        {'nome': 'Carlos Eduardo Mendes', 'codigo': 'CLI004', 'endereco': 'Rua Marechal Deodoro, 321', 'bairro': 'Granbery', 'referencia': 'Próximo ao supermercado', 'telefone': '(32) 96666-3456'}
    ]
    
    clientes = [Cliente.objects.create(**data) for data in clientes_data]
    print(f"\n{len(clientes)} clientes criados.")
    
    # Criar fornecedores
    fornecedores_data = [
        {'nome': 'Distribuidora Farmacêutica ABC', 'codigo': 'FOR001', 'contato': 'Roberto Silva', 'telefone': '(11) 3333-1111', 'email': 'vendas@abc.com.br'},
        {'nome': 'Laboratório XYZ Ltda', 'codigo': 'FOR002', 'contato': 'Fernanda Costa', 'telefone': '(21) 4444-2222', 'email': 'comercial@xyz.com.br'},
        {'nome': 'Medicamentos Nacional', 'codigo': 'FOR003', 'contato': 'Paulo Santos', 'telefone': '(31) 5555-3333', 'email': 'pedidos@nacional.com.br'}
    ]

    fornecedores = [Fornecedor.objects.create(**data) for data in fornecedores_data]
    print(f"{len(fornecedores)} fornecedores criados.")

    # Criar produtos
    produtos_data = [
        {'nome': 'Dipirona 500mg - Caixa com 20 comprimidos', 'codigo': 'MED001', 'descricao': 'Analgésico e antitérmico', 'preco_base': Decimal('12.50'), 'categoria': 'Analgésicos'},
        {'nome': 'Paracetamol 750mg - Caixa com 10 comprimidos', 'codigo': 'MED002', 'descricao': 'Analgésico e antitérmico', 'preco_base': Decimal('8.90'), 'categoria': 'Analgésicos'},
        {'nome': 'Omeprazol 20mg - Caixa com 14 cápsulas', 'codigo': 'MED003', 'descricao': 'Inibidor da bomba de prótons', 'preco_base': Decimal('25.80'), 'categoria': 'Gastroenterologia'},
        {'nome': 'Losartana 50mg - Caixa com 30 comprimidos', 'codigo': 'MED004', 'descricao': 'Anti-hipertensivo', 'preco_base': Decimal('18.70'), 'categoria': 'Cardiovascular'},
        {'nome': 'Vitamina D3 2000UI - Frasco com 60 cápsulas', 'codigo': 'VIT001', 'descricao': 'Suplemento vitamínico', 'preco_base': Decimal('35.90'), 'categoria': 'Vitaminas'},
        {'nome': 'Protetor Solar FPS 60 - 120ml', 'codigo': 'COS001', 'descricao': 'Proteção solar facial e corporal', 'preco_base': Decimal('42.50'), 'categoria': 'Cosméticos'}
    ]
    
    produtos = [Produto.objects.create(**data) for data in produtos_data]
    print(f"{len(produtos)} produtos criados.")

    # Criar encomendas
    encomendas_data = [
        {'cliente': clientes[0], 'responsavel_criacao': 'João da Silva', 'status': 'criada', 'observacoes': 'Cliente solicitou entrega urgente'},
        {'cliente': clientes[1], 'responsavel_criacao': 'Maria Oliveira', 'status': 'cotacao', 'observacoes': 'Verificar disponibilidade no estoque'},
        {'cliente': clientes[2], 'responsavel_criacao': 'João da Silva', 'status': 'aprovada', 'observacoes': 'Pagamento confirmado via PIX'},
        {'cliente': clientes[3], 'responsavel_criacao': 'Carlos Pereira', 'status': 'entregue', 'observacoes': 'Entrega realizada com sucesso'}
    ]
    
    encomendas = [Encomenda.objects.create(**data) for data in encomendas_data]
    print(f"\n{len(encomendas)} encomendas criadas.")

    # Criar itens das encomendas
    itens_data = [
        {'encomenda': encomendas[0], 'produto': produtos[0], 'fornecedor': fornecedores[0], 'quantidade': 2, 'preco_cotado': Decimal('12.00'), 'observacoes': 'Desconto de 4%'},
        {'encomenda': encomendas[0], 'produto': produtos[2], 'fornecedor': fornecedores[1], 'quantidade': 1, 'preco_cotado': Decimal('24.90')},
        {'encomenda': encomendas[1], 'produto': produtos[1], 'fornecedor': fornecedores[0], 'quantidade': 3, 'preco_cotado': Decimal('8.50'), 'observacoes': 'Promoção'},
        {'encomenda': encomendas[1], 'produto': produtos[4], 'fornecedor': fornecedores[2], 'quantidade': 1, 'preco_cotado': Decimal('34.90')},
        {'encomenda': encomendas[2], 'produto': produtos[3], 'fornecedor': fornecedores[1], 'quantidade': 2, 'preco_cotado': Decimal('18.00'), 'observacoes': 'Medicamento de uso contínuo'},
        {'encomenda': encomendas[2], 'produto': produtos[5], 'fornecedor': fornecedores[2], 'quantidade': 1, 'preco_cotado': Decimal('40.00'), 'observacoes': 'Desconto especial'},
        {'encomenda': encomendas[3], 'produto': produtos[0], 'fornecedor': fornecedores[0], 'quantidade': 1, 'preco_cotado': Decimal('12.50')},
    ]
    
    for data in itens_data:
        ItemEncomenda.objects.create(**data)
    print(f"{len(itens_data)} itens de encomenda criados.")
    
    # Criar entregas
    entregas_data = [
        {'encomenda': encomendas[2], 'data_entrega': date.today() + timedelta(days=1), 'responsavel_entrega': 'Entregador José', 'valor_pago_adiantamento': Decimal('50.00'), 'data_prevista': date.today() + timedelta(days=1), 'observacoes_entrega': 'Entregar no período da manhã'},
        {'encomenda': encomendas[3], 'data_entrega': date.today() - timedelta(days=1), 'responsavel_entrega': 'Entregador José', 'valor_pago_adiantamento': Decimal('10.00'), 'data_entrega_realizada': date.today() - timedelta(days=1), 'hora_entrega': datetime.now().time(), 'entregue_por': 'José Silva', 'assinatura_cliente': 'Assinado por Carlos E. Mendes', 'data_prevista': date.today() - timedelta(days=1), 'data_realizada': datetime.now() - timedelta(days=1), 'observacoes_entrega': 'Entrega realizada sem problemas'}
    ]
    
    for data in entregas_data:
        Entrega.objects.create(**data)
    print(f"{len(entregas_data)} entregas criadas.")
    
    print("\n--- Dados de exemplo criados com sucesso! ---")

if __name__ == '__main__':
    criar_dados_exemplo()