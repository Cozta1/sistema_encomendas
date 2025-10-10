# Sistema de Encomendas - Drogaria Benfica

## Visão Geral

O **Sistema de Encomendas da Drogaria Benfica** é uma aplicação web desenvolvida em Django que digitaliza e moderniza o processo de gerenciamento de encomendas farmacêuticas. O sistema foi criado baseado no formulário físico original da drogaria, mantendo a familiaridade visual enquanto adiciona funcionalidades digitais avançadas.

## Características Principais

### 📋 Gestão Completa de Encomendas
- **Criação e edição** de encomendas com interface intuitiva
- **Múltiplos status** de acompanhamento (Criada, Em Cotação, Aprovada, Em Andamento, Pronta para Entrega, Entregue, Cancelada)
- **Formulário digital** que replica fielmente o documento físico original
- **Cálculo automático** de valores totais e restantes

### 👥 Gerenciamento de Clientes
- Cadastro completo com endereço, bairro, telefone e referências
- Histórico de encomendas por cliente
- Busca e filtros avançados

### 📦 Catálogo de Produtos
- Organização por categorias (Analgésicos, Cardiovascular, Vitaminas, etc.)
- Controle de preços base e códigos
- Rastreamento de uso em encomendas

### 🚚 Controle de Entregas
- **Programação de entregas** com data, hora e responsável
- **Controle financeiro** com adiantamentos e valores restantes
- **Confirmação de entrega** com assinatura do cliente
- **Histórico completo** de entregas realizadas

### 🏢 Gestão de Fornecedores
- Cadastro de fornecedores com dados de contato
- Controle de cotações por fornecedor
- Histórico de relacionamento comercial

## Tecnologias Utilizadas

- **Backend**: Django 5.2.7 com Python 3.11
- **Frontend**: HTML5, CSS3, JavaScript e Bootstrap 5
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Interface**: Design responsivo com tema personalizado
- **Ícones**: Bootstrap Icons

## Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Django 5.2+
- Navegador web moderno

### Passos de Instalação

1. **Clone ou baixe o projeto**
```bash
cd sistema_encomendas
```

2. **Instale as dependências**
```bash
cd sistema_encomendas
```

3. **Execute as migrações**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Crie dados de exemplo (opcional)**
```bash
python populate_db.py
```

5. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

6. **Execute o servidor**
```bash
python manage.py runserver
```

7. **Acesse o sistema**
- Sistema: http://localhost:8000
- Admin: http://localhost:8000/admin

## Estrutura do Projeto

```
sistema_encomendas/
├── sistema_encomendas/          # Configurações do projeto
├── encomendas/                  # App principal
│   ├── models.py                # Modelos de dados
│   ├── views.py                 # Views e lógica de negócio
│   ├── forms.py                 # Formulários Django
│   ├── urls.py                  # URLs do app
│   └── templates/encomendas/    # Templates HTML
├── populate_db.py               # Script para dados de exemplo
└── README.md                    # Esta documentação
```

## Funcionalidades Implementadas

### Dashboard Interativo
- **Visão geral** com estatísticas em tempo real
- **Últimas encomendas** com acesso rápido
- **Ações rápidas** para criação de novos registros
- **Navegação intuitiva** entre módulos

### Sistema de Encomendas
- ✅ **Listagem** com filtros por status, cliente e busca textual
- ✅ **Criação** com formulário dinâmico de múltiplos itens
- ✅ **Edição** completa de dados e itens
- ✅ **Visualização detalhada** replicando o formulário físico
- ✅ **Exclusão** com confirmação e avisos de segurança
- ✅ **Impressão** otimizada para documentos físicos

### Gestão de Entregas
- ✅ **Programação** com data, hora e responsável
- ✅ **Controle financeiro** automático
- ✅ **Confirmação** de entrega realizada
- ✅ **Histórico** completo de entregas

### Interface Responsiva
- ✅ **Design mobile-first** compatível com tablets e smartphones
- ✅ **Tema personalizado** com cores da Drogaria Benfica
- ✅ **Navegação intuitiva** com sidebar e breadcrumbs
- ✅ **Feedback visual** com status coloridos e ícones

## Uso do Sistema

### Fluxo Básico de Trabalho

1. **Cadastro de Clientes**: Registre os dados dos clientes com endereços completos
2. **Cadastro de Produtos**: Mantenha o catálogo atualizado com preços e categorias
3. **Cadastro de Fornecedores**: Registre fornecedores com dados de contato
4. **Criação de Encomendas**: 
   - Selecione o cliente
   - Adicione produtos com quantidades e preços cotados
   - Defina o responsável e observações
5. **Gestão de Status**: Acompanhe o progresso através dos status
6. **Programação de Entregas**: Configure data, responsável e valores
7. **Confirmação de Entrega**: Registre a entrega realizada

## Dados de Exemplo

O sistema inclui um script `populate_db.py` que cria dados de exemplo para demonstração:

- **4 Clientes** com endereços completos
- **3 Fornecedores** com dados de contato
- **6 Produtos** de diferentes categorias
- **4 Encomendas** em diferentes status
- **7 Itens** distribuídos nas encomendas
- **2 Entregas** (uma programada, uma realizada)

## Personalização

### Cores e Tema
O sistema utiliza um tema personalizado baseado nas cores da Drogaria Benfica:
- **Azul Principal**: #2c5aa0 (cor do logotipo)
- **Verde Sucesso**: #28a745 (entregas e aprovações)
- **Laranja Atenção**: #fd7e14 (cotações e pendências)
- **Vermelho Alerta**: #dc3545 (cancelamentos e exclusões)

### Logotipo e Identidade
- Logotipo "+B DROGARIA Benfica" integrado ao cabeçalho
- Telefones de contato: (32) 99994-3178, (32) 3112-3999, (32) 3272-8532
- Slogan: "Entrega em toda Juiz de Fora"

## Conclusão

O **Sistema de Encomendas da Drogaria Benfica** representa uma modernização completa do processo manual, mantendo a familiaridade visual do formulário original enquanto adiciona eficiência digital. O sistema oferece:

- **Interface intuitiva** baseada no formulário físico conhecido
- **Funcionalidades completas** para gestão de encomendas
- **Design responsivo** para uso em qualquer dispositivo
- **Dados organizados** com relacionamentos bem definidos
- **Escalabilidade** para crescimento futuro

O projeto demonstra como a tecnologia pode melhorar processos tradicionais sem perder a essência e familiaridade que os usuários valorizam.

---

**Desenvolvido com Django e dedicação para a Drogaria Benfica**  
*Sistema criado em outubro de 2025*
