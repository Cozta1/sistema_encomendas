#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo, incluindo usuários personalizados
e associando os dados a cada usuário.
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
    ItemEncomenda.objects.all().delete()
    Entrega.objects.all().delete()
    Encomenda.objects.all().delete()
    Produto.objects.all().delete()
    Fornecedor.objects.all().delete()
    Cliente.objects.all().delete()
    CustomUser.objects.filter(is_superuser=False).delete()
    
    print("\n--- Criando dados de exemplo ---")

    # Criar Usuários
    users_data = [
        {'username': 'joao.farma', 'password': 'Password123', 'nome_completo': 'João da Silva', 'cargo': 'Farmacêutico', 'identificacao': 'CRF-MG 12345'},
        {'username': 'maria.atendente', 'password': 'Password123', 'nome_completo': 'Maria Oliveira', 'cargo': 'Atendente', 'identificacao': 'ATD-001'},
    ]

    users = []
    for data in users_data:
        try:
            user = CustomUser.objects.create_user(**data)
            users.append(user)
            print(f"Usuário criado: {user.username}")
        except Exception as e:
            # Se o usuário já existir, apenas o busca
            user = CustomUser.objects.get(username=data['username'])
            users.append(user)
            print(f"Usuário {user.username} já existe, utilizando-o.")
            
    # Atribui os usuários criados para facilitar a leitura
    user_joao = users[0]
    user_maria = users[1]

    # Criar clientes (associando cada um a um usuário)
    clientes_data = [
        {'user': user_joao, 'nome': 'Maria Silva Santos', 'codigo': 'CLI001', 'endereco': 'Rua das Flores, 123', 'bairro': 'Centro', 'telefone': '(32) 99999-1234'},
        {'user': user_joao, 'nome': 'Carlos Eduardo Mendes', 'codigo': 'CLI004', 'endereco': 'Rua Marechal Deodoro, 321', 'bairro': 'Granbery', 'telefone': '(32) 96666-3456'},
        {'user': user_maria, 'nome': 'João Carlos Oliveira', 'codigo': 'CLI002', 'endereco': 'Av. Presidente Vargas, 456', 'bairro': 'São Mateus', 'telefone': '(32) 98888-5678'},
        {'user': user_maria, 'nome': 'Ana Paula Costa', 'codigo': 'CLI003', 'endereco': 'Rua São João, 789', 'bairro': 'Benfica', 'telefone': '(32) 97777-9012'}
    ]
    
    clientes = [Cliente.objects.create(**data) for data in clientes_data]
    print(f"\n{len(clientes)} clientes criados e associados a usuários.")
    
    # Criar fornecedores (associando a usuários)
    fornecedores_data = [
        {'user': user_joao, 'nome': 'Distribuidora Farmacêutica ABC', 'codigo': 'FOR001', 'contato': 'Roberto Silva'},
        {'user': user_maria, 'nome': 'Laboratório XYZ Ltda', 'codigo': 'FOR002', 'contato': 'Fernanda Costa'},
        {'user': user_joao, 'nome': 'Medicamentos Nacional', 'codigo': 'FOR003', 'contato': 'Paulo Santos'}
    ]

    fornecedores = [Fornecedor.objects.create(**data) for data in fornecedores_data]
    print(f"{len(fornecedores)} fornecedores criados e associados a usuários.")

    # Criar produtos (associando a usuários)
    produtos_data = [
        {'user': user_joao, 'nome': 'Dipirona 500mg', 'codigo': 'MED001', 'preco_base': Decimal('12.50'), 'categoria': 'Analgésicos'},
        {'user': user_maria, 'nome': 'Paracetamol 750mg', 'codigo': 'MED002', 'preco_base': Decimal('8.90'), 'categoria': 'Analgésicos'},
        {'user': user_joao, 'nome': 'Omeprazol 20mg', 'codigo': 'MED003', 'preco_base': Decimal('25.80'), 'categoria': 'Gastro'},
        {'user': user_maria, 'nome': 'Losartana 50mg', 'codigo': 'MED004', 'preco_base': Decimal('18.70'), 'categoria': 'Cardio'},
        {'user': user_joao, 'nome': 'Vitamina D3 2000UI', 'codigo': 'VIT001', 'preco_base': Decimal('35.90'), 'categoria': 'Vitaminas'},
    ]
    
    produtos = [Produto.objects.create(**data) for data in produtos_data]
    print(f"{len(produtos)} produtos criados e associados a usuários.")

    # Criar encomendas (associando a usuários e seus respectivos clientes)
    encomendas_data = [
        {'user': user_joao, 'cliente': clientes[0], 'responsavel_criacao': user_joao.nome_completo, 'status': 'criada'},
        {'user': user_maria, 'cliente': clientes[2], 'responsavel_criacao': user_maria.nome_completo, 'status': 'cotacao'},
        {'user': user_joao, 'cliente': clientes[1], 'responsavel_criacao': user_joao.nome_completo, 'status': 'entregue'},
    ]
    
    encomendas = [Encomenda.objects.create(**data) for data in encomendas_data]
    print(f"\n{len(encomendas)} encomendas criadas e associadas a usuários.")

    # Criar itens das encomendas
    itens_data = [
        {'encomenda': encomendas[0], 'produto': produtos[0], 'fornecedor': fornecedores[0], 'quantidade': 2, 'preco_cotado': Decimal('12.00')},
        {'encomenda': encomendas[0], 'produto': produtos[2], 'fornecedor': fornecedores[2], 'quantidade': 1, 'preco_cotado': Decimal('24.90')},
        {'encomenda': encomendas[1], 'produto': produtos[1], 'fornecedor': fornecedores[1], 'quantidade': 3, 'preco_cotado': Decimal('8.50')},
        {'encomenda': encomendas[2], 'produto': produtos[0], 'fornecedor': fornecedores[0], 'quantidade': 1, 'preco_cotado': Decimal('12.50')},
    ]
    
    for data in itens_data:
        ItemEncomenda.objects.create(**data)
    print(f"{len(itens_data)} itens de encomenda criados.")
    
    # Criar entrega para a encomenda entregue
    Entrega.objects.create(
        encomenda=encomendas[2],
        data_entrega=date.today() - timedelta(days=1),
        responsavel_entrega='Entregador Carlos',
        data_entrega_realizada=date.today() - timedelta(days=1),
        hora_entrega=datetime.now().time(),
        entregue_por='Carlos Silva',
        assinatura_cliente='Assinado pelo cliente.'
    )
    print("1 entrega criada.")
    
    print("\n--- Dados de exemplo criados com sucesso! ---")

if __name__ == '__main__':
    criar_dados_exemplo()