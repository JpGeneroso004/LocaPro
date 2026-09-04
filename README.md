# 🎪 Art.Tendas — Sistema de Gestão de Eventos

Sistema web completo para gerenciar eventos, inventário de tendas e placas de palco/piso da empresa Art.Tendas. 
Originalmente concebido como uma ferramenta interna, o projeto está em evolução para se tornar um **SaaS (Software as a Service)** focado no nicho de locação para eventos.

---

## 🚀 Visão de Futuro: Evolução para SaaS

O objetivo é transformar este sistema em um produto comercializável para outras empresas do ramo de locação de estruturas. Para isso, o sistema evoluirá para uma arquitetura **Multi-tenant** (múltiplos inquilinos), garantindo que diferentes empresas possam usar a mesma plataforma com dados totalmente isolados.

### 🗺️ Roadmap do SaaS
- [ ] **Autenticação e Gestão de Usuários:** Sistema de login seguro com níveis de acesso (Admin, Funcionário, etc.).
- [ ] **Arquitetura Multi-tenant:** Separação de dados por empresa (Tenant), garantindo privacidade e segurança (possivelmente usando esquemas de banco de dados ou filtragem por ID da empresa).
- [ ] **Módulo Financeiro/Faturamento:** Controle de pagamentos, geração de orçamentos e faturas.
- [ ] **Planos e Assinaturas (Billing):** Integração com gateway de pagamento para cobrar as empresas que usam o software.
- [ ] **Painel Super-Admin:** Dashboard para o dono do SaaS gerenciar as empresas cadastradas, assinaturas ativas e métricas globais.
- [ ] **Relatórios Avançados:** Exportação de dados e gráficos de desempenho para os clientes.

---

## 📋 Funcionalidades Atuais

- **Dashboard** com estatísticas em tempo real e mapa interativo de eventos
- **Gestão de Eventos** — criar, editar, visualizar e excluir eventos com localização geográfica
- **Inventário de Tendas** — cadastrar e controlar tendas 3×3 a 10×10 m (exceto 9×9)
- **Inventário de Placas** — gerenciar até 30 placas de palco/piso
- **Mapa Interativo** (OpenStreetMap via Leaflet) — visualize onde estão seus eventos
- **Controle de Status** — disponível, em uso, em manutenção (atualizado automaticamente)
- **Busca e Filtros** na listagem de eventos
- **Admin Django** para gerenciamento avançado

---

## 🛠️ Como Rodar (Desenvolvimento)

### Pré-requisitos
- Python 3.10 ou superior
- pip

### Instalação Manual

```bash
# Entrar na pasta do projeto django
cd arttendas

# Criar e ativar ambiente virtual
python -m venv venv
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
/
├── README.md           # Esta documentação
├── .gitignore          # Arquivos ignorados pelo git
└── arttendas/          # Projeto Django
    ├── core/               # Configurações Django
    ├── eventos/            # App de eventos
    ├── inventario/         # App de inventário
    ├── templates/          # HTML (base + apps)
    ├── static/             # CSS, JS, imagens
    └── requirements.txt    # Dependências do Python
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

Acesse `/admin/` com as credenciais criadas para gerenciar todos os dados diretamente.

---

Desenvolvido com ❤️ para Art.Tendas — Formosa, GO
