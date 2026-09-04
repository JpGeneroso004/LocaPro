#!/bin/bash
# ============================================
#  Art.Tendas — Script de Configuração Inicial
# ============================================
echo ""
echo "  ████████╗███████╗███╗   ██╗██████╗  █████╗ ███████╗"
echo "  ╚══██╔══╝██╔════╝████╗  ██║██╔══██╗██╔══██╗██╔════╝"
echo "     ██║   █████╗  ██╔██╗ ██║██║  ██║███████║███████╗"
echo "     ██║   ██╔══╝  ██║╚██╗██║██║  ██║██╔══██║╚════██║"
echo "     ██║   ███████╗██║ ╚████║██████╔╝██║  ██║███████║"
echo "     ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚══════╝"
echo ""
echo "  Art.Tendas — Sistema de Gestão de Eventos"
echo "  ==========================================="
echo ""

# 1. Criar venv
echo "📦 Criando ambiente virtual..."
python3 -m venv venv

# 2. Ativar venv
echo "⚡ Ativando ambiente virtual..."
source venv/bin/activate

# 3. Instalar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt --quiet

# 4. Migrations
echo "🗄️  Aplicando migrações..."
python manage.py makemigrations
python manage.py migrate

# 5. Dados de demonstração
echo "🌱 Inserindo dados de demonstração..."
python manage.py seed_data

# 6. Superusuário
echo ""
echo "👤 Criar superusuário para o Admin Django:"
python manage.py createsuperuser

echo ""
echo "✅ Tudo pronto! Para iniciar o servidor:"
echo ""
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "   Acesse: http://127.0.0.1:8000"
echo "   Admin:  http://127.0.0.1:8000/admin"
echo ""
