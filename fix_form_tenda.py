import os

templates_dir = r"C:\ArtTendas\arttendas\templates\inventario"

form_tenda_html = """{% extends 'base.html' %}
{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="d-flex align-items-center mb-4">
  <a href="javascript:history.back()" class="btn btn-light rounded-circle me-3 shadow-sm"><i class="bi bi-arrow-left"></i></a>
  <h3 class="fw-bold mb-0">{{ titulo }}</h3>
</div>

<div class="card shadow-sm border-0 p-4 mb-5">
  <form method="post">
    {% csrf_token %}
    
    {% if form.errors %}
      <div class="alert alert-danger mb-4">
        <strong>Verifique os erros abaixo:</strong>
        {{ form.errors }}
      </div>
    {% endif %}

    <div class="mb-3">
      <label class="form-label fw-bold">Tamanho</label>
      {{ form.tamanho }}
    </div>
    
    <div class="mb-3">
      <label class="form-label fw-bold">Tipo</label>
      {{ form.tipo }}
    </div>

    <div class="mb-3">
      <label class="form-label fw-bold">Status</label>
      {{ form.status }}
    </div>

    <div class="mb-4">
      <label class="form-label fw-bold">Observações</label>
      {{ form.observacoes }}
    </div>

    <div class="d-grid mt-4">
      <button type="submit" class="btn btn-warning btn-lg shadow fw-bold">SALVAR TENDA</button>
    </div>
  </form>
</div>
{% endblock %}
"""

with open(os.path.join(templates_dir, "form_tenda.html"), "w", encoding="utf-8") as f:
    f.write(form_tenda_html)
