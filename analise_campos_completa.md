# Análise Completa dos Campos do Formulário Físico

## Campos Identificados no Formulário Original

### Cabeçalho
- **Número da Encomenda**: 1700 (campo destacado no canto superior direito)
- **Data**: ___/___/___ (campo no cabeçalho)
- **Responsável**: (campo no cabeçalho)

### Seção Principal - Produtos e Fornecedores
1. **Produto**: (linha com espaço longo)
2. **Código**: (do produto)
3. **Preço**: (do produto)
4. **Fornecedor Cotado**: (linha com espaço longo)
5. **Código**: (do fornecedor)
6. **Preço**: (cotado pelo fornecedor)

### Seção do Cliente
7. **Nome do Cliente**: (linha longa)
8. **Código**: (do cliente)
9. **End.**: (endereço completo)
10. **Bairro**: (campo à esquerda)
11. **Referência**: (campo à direita, na mesma linha do bairro)

### Seção de Pagamento e Entrega
12. **Valor Pago Adiantamento**: (linha longa)
13. **Data Entrega**: ___/___/___ (formato de data)
14. **Observação**: (linha longa)
15. **Responsável Entrega**: (linha longa)
16. **Data**: ___/___/___ (da entrega)
17. **Hora**: (da entrega)
18. **Ass. do Cliente**: (linha para assinatura)

### Seção Inferior Destacada (Caixa com número 1700)
19. **Responsável pela Encomenda**: (linha longa)
20. **Valor do Adiantamento**: (linha longa)
21. **Data**: ___/___/___ (repetida)
22. **Hora**: (repetida)
23. **Valor do Produto**: (linha longa)
24. **Entregue por**: (linha longa)

## Campos Ausentes no Sistema Atual

### Campos de Produto que precisam ser adicionados:
- **Código do Produto** (já existe)
- **Preço do Produto** (já existe como preco_base)

### Campos de Fornecedor que precisam ser adicionados:
- **Código do Fornecedor** (já existe)
- **Preço Cotado pelo Fornecedor** (já existe como preco_cotado)

### Campos de Cliente que precisam ser adicionados:
- **Código do Cliente** (já existe)
- **Referência** (já existe)

### Campos de Entrega que precisam ser melhorados:
- **Hora da Entrega** (precisa ser mais específico)
- **Assinatura do Cliente** (já existe como boolean)
- **Entregue por** (já existe)

### Campos que precisam ser adicionados:
1. **Telefone do Cliente** (não está no formulário físico, mas é útil)
2. **Observações da Encomenda** (campo "Observação" do formulário)
3. **Hora específica da entrega** (separada da data)

## Conclusão da Análise

O sistema atual já contempla a maioria dos campos do formulário físico. Os principais ajustes necessários são:

1. **Melhorar a exibição dos códigos** nos formulários
2. **Separar hora da data** na entrega
3. **Garantir que todos os campos sejam editáveis** nos formulários
4. **Ajustar o layout** para corresponder exatamente ao formulário físico
5. **Adicionar campos de observação** mais específicos
