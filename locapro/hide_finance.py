
with open("templates/eventos/dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

old_fin = """<div class="row g-2 mb-3">
  <div class="col-6">
    <div class="card h-100 bg-success text-white p-3 shadow-sm border-0">
      <small class="fw-bold text-white-50 text-uppercase">Faturamento no Mês</small>
      <h3 class="fw-bold mb-0 mt-1">R$ {{ faturamento_mes|floatformat:2 }}</h3>
    </div>
  </div>
  <div class="col-6">
    <div class="card h-100 bg-dark text-white p-3 shadow-sm border-0">
      <small class="fw-bold text-white-50 text-uppercase">Receita Futura Prevista</small>
      <h3 class="fw-bold text-warning mb-0 mt-1">R$ {{ previsao_faturamento|floatformat:2 }}</h3>
    </div>
  </div>
</div>"""

new_fin = """{% if user.cargo == "dono" or user.cargo == "gerente" %}
<div class="row g-2 mb-3">
  <div class="col-6">
    <div class="card h-100 bg-success text-white p-3 shadow-sm border-0">
      <small class="fw-bold text-white-50 text-uppercase">Faturamento no Mês</small>
      <h3 class="fw-bold mb-0 mt-1">R$ {{ faturamento_mes|floatformat:2 }}</h3>
    </div>
  </div>
  <div class="col-6">
    <div class="card h-100 bg-dark text-white p-3 shadow-sm border-0">
      <small class="fw-bold text-white-50 text-uppercase">Receita Futura Prevista</small>
      <h3 class="fw-bold text-warning mb-0 mt-1">R$ {{ previsao_faturamento|floatformat:2 }}</h3>
    </div>
  </div>
</div>
{% endif %}"""

text = text.replace(old_fin, new_fin)

old_ytd = """  <div class="col-md-6">
    <div class="card h-100 bg-primary bg-gradient text-white p-3 shadow-sm border-0 position-relative overflow-hidden">
      <i class="bi bi-graph-up-arrow position-absolute" style="font-size: 4rem; opacity: 0.2; right: -10px; bottom: -10px;"></i>
      <small class="fw-bold text-white-50 text-uppercase">Faturamento Anual (YTD)</small>
      <h3 class="fw-bold mb-0 mt-1">R$ {{ faturamento_ano|floatformat:2 }}</h3>
      <small class="mt-2 text-white"><i class="bi bi-calendar-check"></i> Receita total gerada no ano atual.</small>
    </div>
  </div>"""

new_ytd = """  {% if user.cargo == "dono" or user.cargo == "gerente" %}
  <div class="col-md-6">
    <div class="card h-100 bg-primary bg-gradient text-white p-3 shadow-sm border-0 position-relative overflow-hidden">
      <i class="bi bi-graph-up-arrow position-absolute" style="font-size: 4rem; opacity: 0.2; right: -10px; bottom: -10px;"></i>
      <small class="fw-bold text-white-50 text-uppercase">Faturamento Anual (YTD)</small>
      <h3 class="fw-bold mb-0 mt-1">R$ {{ faturamento_ano|floatformat:2 }}</h3>
      <small class="mt-2 text-white"><i class="bi bi-calendar-check"></i> Receita total gerada no ano atual.</small>
    </div>
  </div>
  {% endif %}"""

text = text.replace(old_ytd, new_ytd)

with open("templates/eventos/dashboard.html", "w", encoding="utf-8") as f:
    f.write(text)

