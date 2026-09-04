import os

templates_dir_eventos = r"C:\ArtTendas\arttendas\templates\eventos"
templates_dir_inventario = r"C:\ArtTendas\arttendas\templates\inventario"

confirmar_exclusao_evento = """{% extends 'base.html' %}
{% block title %}Excluir Evento{% endblock %}

{% block content %}
<div class="card shadow-sm border-0 border-top border-danger border-5 p-4 mb-5 text-center mt-4">
  <div class="mb-4">
    <i class="bi bi-exclamation-triangle-fill text-danger" style="font-size: 3rem;"></i>
  </div>
  <h3 class="fw-bold mb-3">Excluir Evento?</h3>
  <p class="text-muted mb-4">Tem certeza que deseja excluir o evento <strong>"{{ evento.nome }}"</strong>?<br>Esta ação não pode ser desfeita e os equipamentos alocados voltarão a ficar disponíveis.</p>
  
  <form method="post" class="d-flex justify-content-center gap-3">
    {% csrf_token %}
    <a href="{% url 'eventos:detalhe' evento.pk %}" class="btn btn-light fw-bold px-4">Cancelar</a>
    <button type="submit" class="btn btn-danger fw-bold px-4">Sim, Excluir</button>
  </form>
</div>
{% endblock %}
"""

confirmar_exclusao_tenda = """{% extends 'base.html' %}
{% block title %}Excluir Tenda{% endblock %}

{% block content %}
<div class="card shadow-sm border-0 border-top border-danger border-5 p-4 mb-5 text-center mt-4">
  <div class="mb-4">
    <i class="bi bi-exclamation-triangle-fill text-danger" style="font-size: 3rem;"></i>
  </div>
  <h3 class="fw-bold mb-3">Excluir Tenda?</h3>
  <p class="text-muted mb-4">Tem certeza que deseja excluir a tenda <strong>{{ tenda.codigo }}</strong>?<br>Esta ação não pode ser desfeita.</p>
  
  <form method="post" class="d-flex justify-content-center gap-3">
    {% csrf_token %}
    <a href="{% url 'inventario:inventario' %}" class="btn btn-light fw-bold px-4">Cancelar</a>
    <button type="submit" class="btn btn-danger fw-bold px-4">Sim, Excluir</button>
  </form>
</div>
{% endblock %}
"""

confirmar_exclusao_conjunto = """{% extends 'base.html' %}
{% block title %}Excluir Conjunto{% endblock %}

{% block content %}
<div class="card shadow-sm border-0 border-top border-danger border-5 p-4 mb-5 text-center mt-4">
  <div class="mb-4">
    <i class="bi bi-exclamation-triangle-fill text-danger" style="font-size: 3rem;"></i>
  </div>
  <h3 class="fw-bold mb-3">Excluir Conjunto?</h3>
  <p class="text-muted mb-4">Tem certeza que deseja excluir o conjunto <strong>{{ conjunto.nome }}</strong>?<br>Esta ação não pode ser desfeita.</p>
  
  <form method="post" class="d-flex justify-content-center gap-3">
    {% csrf_token %}
    <a href="{% url 'inventario:inventario' %}" class="btn btn-light fw-bold px-4">Cancelar</a>
    <button type="submit" class="btn btn-danger fw-bold px-4">Sim, Excluir</button>
  </form>
</div>
{% endblock %}
"""

with open(os.path.join(templates_dir_eventos, "confirmar_exclusao.html"), "w", encoding="utf-8") as f:
    f.write(confirmar_exclusao_evento)

with open(os.path.join(templates_dir_inventario, "confirmar_exclusao_tenda.html"), "w", encoding="utf-8") as f:
    f.write(confirmar_exclusao_tenda)

with open(os.path.join(templates_dir_inventario, "confirmar_exclusao_conjunto.html"), "w", encoding="utf-8") as f:
    f.write(confirmar_exclusao_conjunto)

print("Telas de exclusão atualizadas!")
