#!/bin/bash

echo "🚀 Configurando Sistema de Encomendas - Drogaria Benfica"
echo "=================================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.11 ou superior."
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Instalar dependências
echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

# Executar migrações
echo "🗄️ Configurando banco de dados..."
python3 manage.py makemigrations
python3 manage.py migrate

# Criar dados de exemplo
echo "📊 Criando dados de exemplo..."
python3 populate_db.py

echo ""
echo "✅ Sistema configurado com sucesso!"
echo ""
echo "Para iniciar o servidor:"
echo "  python3 manage.py runserver"
echo ""
echo "Para acessar o sistema:"
echo "  http://localhost:8000"
echo ""
echo "Para criar um superusuário (admin):"
echo "  python3 manage.py createsuperuser"
echo ""
echo "🎉 Bom uso do Sistema de Encomendas!"
