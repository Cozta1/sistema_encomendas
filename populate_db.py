#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo, incluindo usuários personalizados
e associando os dados à equipe correta.
"""
import os
import django
from decimal import Decimal
from datetime import date, datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_encomendas.settings')
django.setup()

from django.contrib.auth import get_user_model
from encomendas.models import Cliente, Fornecedor, Produto, Encomenda, ItemEncomenda, Entrega, Equipe

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
    Equipe.objects.all().delete()
    
    print("\n--- Criando dados de exemplo ---")

    # --- Equipe 1: Drogaria Benfica - Centro ---
    equipe_centro = Equipe.objects.create(nome="Drogaria Benfica - Centro")
    print(f"Equipe criada: {equipe_centro.nome}")

    user_joao = CustomUser.objects.create_user(
        username='joao.farma', password='Password123', nome_completo='João da Silva',
        cargo='Farmacêutico', identificacao='CRF-MG 12345', equipe=equipe_centro
    )
    user_maria = CustomUser.objects.create_user(
        username='maria.atendente', password='Password123', nome_completo='Maria Oliveira',
        cargo='Atendente', identificacao='ATD-001', equipe=equipe_centro
    )
    print(f"Usuários criados e associados à equipe '{equipe_centro.nome}': {user_joao.username}, {user_maria.username}")

    # Dados para a Equipe Centro
    clientes_centro = [
        Cliente.objects.create(
            equipe=equipe_centro, nome='Maria Silva Santos', cpf='111.222.333-44', 
            rua='Rua das Flores', numero='123', complemento='Apt 201', bairro='Centro', 
            referencia='Próximo ao Banco do Brasil', telefone='(32) 99999-1234'
        ),
        Cliente.objects.create(
            equipe=equipe_centro, nome='Carlos Eduardo Mendes', cpf='222.333.444-55',
            rua='Rua Marechal Deodoro', numero='321', bairro='Granbery', 
            referencia='Próximo ao supermercado', telefone='(32) 96666-3456'
        )
    ]
    fornecedores_centro = [
        Fornecedor.objects.create(equipe=equipe_centro, nome='Distribuidora Farmacêutica ABC', codigo='FOR001', contato='Roberto Silva'),
        Fornecedor.objects.create(equipe=equipe_centro, nome='Medicamentos Nacional', codigo='FOR003', contato='Paulo Santos')
    ]
    produtos_centro = [
        Produto.objects.create(equipe=equipe_centro, nome='Dipirona 500mg', codigo='MED001', preco_base=Decimal('12.50')),
        Produto.objects.create(equipe=equipe_centro, nome='Omeprazol 20mg', codigo='MED003', preco_base=Decimal('25.80')),
        Produto.objects.create(equipe=equipe_centro, nome='Vitamina D3 2000UI', codigo='VIT001', preco_base=Decimal('35.90'))
    ]
    
    encomenda_centro = Encomenda.objects.create(
        equipe=equipe_centro, cliente=clientes_centro[0], responsavel_criacao=user_joao, 
        status='entregue', valor_pago_adiantamento=Decimal('10.00'), data_prevista_entrega=date.today() - timedelta(days=1)
    )
    ItemEncomenda.objects.create(encomenda=encomenda_centro, produto=produtos_centro[0], fornecedor=fornecedores_centro[0], quantidade=2, preco_cotado=Decimal('12.00'))
    encomenda_centro.calcular_valor_total()
    
    Entrega.objects.create(
        encomenda=encomenda_centro,
        responsavel_entrega='Entregador Carlos',
        data_entrega_realizada=date.today() - timedelta(days=1),
        hora_entrega=datetime.now().time(),
        entregue_por='Carlos Silva',
        assinatura_cliente='Assinado pelo cliente.'
    )

    print(f"\nDados criados para a equipe '{equipe_centro.nome}'.")
    
    print("\n--- Dados de exemplo criados com sucesso! ---")

if __name__ == '__main__':
    criar_dados_exemplo()