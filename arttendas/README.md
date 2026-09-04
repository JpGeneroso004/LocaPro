# 🎪 Art.Tendas — Sistema de Gestão de Eventos

Sistema web completo para gerenciar eventos, inventário de tendas e placas de palco/piso da empresa Art.Tendas.

---

## 📋 Funcionalidades

- **Dashboard** com estatísticas em tempo real e mapa interativo de eventos
- **Gestão de Eventos** — criar, editar, visualizar e excluir eventos com localização geográfica
- **Inventário de Tendas** — cadastrar e controlar tendas 3×3 a 10×10 m (exceto 9×9)
- **Inventário de Placas** — gerenciar até 30 placas de palco/piso
- **Mapa Interativo** (OpenStreetMap via Leaflet) — visualize onde estão seus eventos
- **Controle de Status** — disponível, em uso, em manutenção (atualizado automaticamente)
- **Busca e Filtros** na listagem de eventos
- **Admin Django** para gerenciamento avançado

---

## 🚀 Como Rodar

### Pré-requisitos
- Python 3.10 ou superior
- pip

### Instalação Automática (recomendado)

```bash
# 1. Dar permissão ao script
chmod +x setup.sh

# 2. Rodar o setup (cria venv, instala, migra, popula dados)
./setup.sh

# 3. Iniciar o servidor
source venv/bin/activate
python manage.py runserver
```

### Instalação Manual

```bash
# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate          # Linux/Mac
# ou: venv\Scripts\activate       # Windows

# Instalar dependências
pip install -r requirements.txt

# Criar banco de dados
python manage.py makemigrations
python manage.py migrate

# Popular com dados de demonstração
python manage.py seed_data

# Criar usuário administrador
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000**

---

## 🗂️ Estrutura do Projeto

```
arttendas/
├── core/               # Configurações Django
├── eventos/            # App de eventos
│   ├── management/     # Comando seed_data
│   ├── models.py       # Modelo Evento
│   ├── views.py        # Dashboard, lista, detalhe, CRUD
│   └── forms.py        
├── inventario/         # App de inventário
│   ├── models.py       # Tenda, PlacaPalco
│   ├── views.py        # CRUD de tendas e placas
│   └── forms.py        
├── templates/          # HTML (base + apps)
├── static/             # CSS, JS, imagens
│   ├── css/style.css   # Design system completo
│   ├── js/main.js      
│   └── img/logo.png    # Logo Art.Tendas
├── requirements.txt    
└── setup.sh            # Script de instalação
```

---

## 🎨 Design

- **Paleta:** Preto `#0A0A0A` · Amarelo `#FFD600` · Branco `#FFFFFF`
- **Tipografia:** Barlow Condensed (títulos) · Inter (corpo)
- **Mapa:** Leaflet + OpenStreetMap (gratuito, sem API key)
- **Responsivo:** funciona em mobile, tablet e desktop

---

## 🗺️ Usando o Mapa

Para que um evento apareça no mapa, preencha **Latitude** e **Longitude** ao criar/editar o evento.

Como obter as coordenadas:
1. Abra o [Google Maps](https://maps.google.com)
2. Clique com o botão direito no local
3. Copie as coordenadas (ex: `-15.5362, -47.3344`)

---

## ⚙️ Admin Django

Acesse `/admin/` com as credenciais criadas no setup para gerenciar todos os dados diretamente.

---

Desenvolvido com ❤️ para Art.Tendas — Formosa, GO
