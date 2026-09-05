# ⛺ LocaPro — SaaS de Gestão para Locadoras de Estruturas

O **LocaPro** (anteriormente Art.Tendas) é uma plataforma SaaS (Software as a Service) de nível empresarial, projetada arquitetonicamente para resolver os maiores gargalos logísticos, contratuais e financeiros de empresas de locação de tendas, palcos e estruturas para eventos.

---

## 🚀 Principais Features e Diferenciais do Produto

O sistema vai muito além de um simples CRUD. Ele atua como o sistema nervoso central da locadora:

*   **🛡️ Arquitetura Multi-Tenant Rigorosa:** Um único servidor suporta múltiplas empresas. Os dados são totalmente isolados via `TenantManager` customizado, garantindo que nenhum vazamento de informações (IDOR) ocorra entre locadoras.
*   **🧠 Motor Inteligente de Estoque (com Cache):** O algoritmo varre o banco de dados e calcula sobreposições de datas (incluindo *buffers* logísticos de 24h). Integrado com `django.core.cache` (Memcached local) para checagens de disponibilidade ultrarrápidas (aliviando queries complexas no banco).
*   **✍️ Contratos com Assinatura Eletrônica:** Geração em tempo real do layout do contrato. Conta com uma rota pública *mobile-first* (`/assinatura/`) que permite envio pelo WhatsApp, capturando aceite jurídico (IP + Data) e exibindo QR Code PIX instantâneo.
*   **📊 DRE Financeiro Integrado:** Dashboard em tempo real mostrando Faturamento Bruto Anual (YTD), adiantamentos (Sinal recebido), balanço a receber e inadimplências. Totalmente protegido contra problemas de N+1 queries (`select_related`).
*   **📍 Logística Espacial (Geocoding):** Conversão assíncrona (`threading`) de endereços de eventos em coordenadas geográficas via OpenStreetMap, gerando mapas interativos para a equipe de montagem via Leaflet.js.
*   **💸 Assinaturas e Webhooks de Cobrança:** Integração completa com o gateway de pagamentos ASAAS. Criação automatizada de `Customers`, `Subscriptions` e `Webhooks` seguros (validação via Token) que bloqueiam automaticamente o acesso de locadoras inadimplentes usando Middlewares.
*   **🏆 Programa de Fidelidade (B2B):** Sistema de acúmulo e resgate de pontos (LocaPoints) permitindo *cashback* e retenção de longo prazo.

---

## 🛠️ Stack Tecnológico e Observabilidade

O projeto atingiu maturidade de produção e conta com as melhores práticas para Cloud:

*   **Backend:** Python 3.10+ e Django 4.2+
*   **Banco de Dados:** PostgreSQL
*   **Serviços de Produção:** Gunicorn (App Server), WhiteNoise (Assets Estáticos rápidos)
*   **Frontend:** Bootstrap 5, Leaflet.js
*   **Observabilidade 24/7:**
    *   **Sentry SDK:** Captura de exceções e erros 500 silenciosos, otimizado para não ferir a LGPD (`send_default_pii=False`).
    *   **Logtail (Better Stack):** Injeção em nuvem dos arquivos de `logging` padronizados, sem necessidade de acessar o terminal.
    *   **Healthchecks:** Rota `/api/health/` para rastreamento de tempo de atividade (Uptime Kuma).

---

## 💻 Como Rodar (Ambiente de Desenvolvimento)

```bash
# 1. Entre na pasta do projeto
cd arttendas

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate          # No Linux/Mac
# venv\Scripts\activate           # No Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as Variáveis de Ambiente (.env na raiz)
# Exemplo de chaves necessárias:
# SECRET_KEY=sua-chave-aqui
# DEBUG=True
# DATABASE_URL=postgres://user:pass@localhost:5432/locapro (Opcional no local)
# ASAAS_API_KEY=sua-chave-api-asaas
# ASAAS_WEBHOOK_TOKEN=seu-token-asaas
# SENTRY_DSN=sua-url-sentry
# LOGTAIL_SOURCE_TOKEN=seu-token-logtail

# 5. Aplique o Banco de Dados (SQLite ou Postgres)
python manage.py makemigrations
python manage.py migrate

# 6. Inicie o Servidor
python manage.py runserver
```

Acesse **http://127.0.0.1:8000** no seu navegador.

---

## ☁️ Deploy (Produção)

O repositório já está configurado para provedores de **PaaS** (Platform as a Service) modernos, como **Railway.app**, **Render** ou **Heroku**.

1. Conecte sua conta GitHub à plataforma desejada.
2. O arquivo `Procfile` nativo (na pasta `arttendas`) fará a inicialização via `Gunicorn`.
3. Certifique-se de preencher a variável `DATABASE_URL` no painel do servidor, além das demais variáveis de integração. O `WhiteNoise` assumirá a entrega dos arquivos CSS/JS.

---
*Engenharia rigorosa. Desenhado para ser o padrão nacional na gestão de infraestruturas.*
