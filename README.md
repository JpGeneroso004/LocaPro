# 🚀 LocaPro — SaaS de Gestão para Locadoras de Estruturas

LocaPro (antigo Art.Tendas) é uma plataforma SaaS (Software as a Service) moderna, focada em resolver os maiores desafios logísticos e de gestão financeira de empresas de locação de tendas, palcos, pisos e infraestrutura para eventos.

---

## 🎯 O que o LocaPro resolve?
Gestão de locação é complexa: choques de datas, controle de inventário distribuído e contratos mal redigidos geram prejuízos constantes. O LocaPro atua como o sistema nervoso central da sua locadora, permitindo:

- **Controle de Estoque Inteligente:** Saiba exatamente quantas tendas e placas estão disponíveis, em uso ou em manutenção em qualquer data.
- **Gestão de Eventos em Mapa:** Visualize logisticamente onde estão suas montagens via integração com OpenStreetMap.
- **Contratos Automatizados:** Gere contratos em PDF instantaneamente com regras de negócio blindadas.
- **Faturamento e Cobrança Integrados:** Integração direta com gateway de pagamento para emissão de cobranças e assinaturas.
- **Programa de Fidelidade (LocaPoints):** Gamificação B2B onde clientes ganham pontos por aluguéis e trocam por descontos (aumentando a retenção).

---

## 🏢 Arquitetura Multi-Tenant
O LocaPro foi projetado para rodar na Nuvem e atender centenas de locadoras simultaneamente com **isolamento de dados rigoroso** (Tenant Isolation).
- Cada locadora (Organização) possui seu próprio ambiente seguro.
- Funcionários só visualizam clientes, eventos e estoques pertencentes à sua empresa.
- Sistema de faturamento por assinatura automatizado (integração Asaas).

---

## 🛠️ Tecnologias Utilizadas
- **Backend:** Python + Django 4
- **Banco de Dados:** PostgreSQL (via Tenant Isolation)
- **Frontend:** HTML5, CSS3, JavaScript (Leaflet.js para Mapas)
- **Integrações:** Asaas (Gateway de Pagamentos API v3), OpenStreetMap (Geocoding)
- **Cloud/Infra (Recomendado):** AWS S3 (armazenamento estático), Redis (Cache), Celery (Tarefas Assíncronas)

---

## 🚀 Como Rodar o Ambiente de Desenvolvimento

### Pré-requisitos
- Python 3.10+
- PostgreSQL (opcional para testes simples, mas obrigatório em produção)

### Instalação

```bash
# Entrar na pasta do projeto django
cd arttendas

# Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate          # Linux/Mac
# ou: venv\Scripts\activate       # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar Variáveis de Ambiente
# Crie um arquivo .env na pasta raiz (baseado no .env.example) com as credenciais do Asaas, DB, etc.

# Executar Migrations
python manage.py makemigrations
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

Acesse: **http://127.0.0.1:8000** e cadastre sua primeira locadora!

---

## 📈 Roadmap de Engenharia (SaaS)
- [x] Isolamento Crítico de Sessões (Middlewares Multi-tenant Seguros)
- [x] Constraints Dinâmicas de Banco de Dados (Prevenção contra Dados Órfãos)
- [x] Integração de Assinaturas Asaas (Webhooks Seguros)
- [ ] Configuração S3 via `django-storages` para Mídias Cloud-Ready
- [ ] Otimização de Geocoding (Mover API do OSM para Workers Celery)
- [ ] Dashboard Avançado de BI para Administradores do SaaS

---

*Desenvolvido para revolucionar a gestão de locadoras de eventos no Brasil.*
