import os

templates_dir = r"C:\ArtTendas\arttendas\templates"

base_html = """{% load static %}
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>{% block title %}Art.Tendas{% endblock %} | Sistema de Gestão</title>
  
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  
  <style>
    body {
      background-color: #f8f9fa;
      padding-bottom: 70px;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .navbar-top {
      background-color: #ffc107;
      box-shadow: 0 2px 4px rgba(0,0,0,.1);
    }
    .navbar-brand {
      font-weight: 900;
      color: #000 !important;
    }
    
    .bottom-nav {
      position: fixed;
      bottom: 0;
      width: 100%;
      background-color: #fff;
      box-shadow: 0 -2px 10px rgba(0,0,0,.1);
      display: flex;
      justify-content: space-around;
      padding: 10px 0;
      z-index: 1000;
    }
    .bottom-nav-item {
      text-align: center;
      color: #6c757d;
      text-decoration: none;
      font-size: 0.85rem;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .bottom-nav-item i {
      font-size: 1.5rem;
      margin-bottom: 2px;
    }
    .bottom-nav-item.active {
      color: #ffc107;
      font-weight: 600;
    }
    
    .card {
      border: none;
      border-radius: 12px;
      box-shadow: 0 4px 6px rgba(0,0,0,.05);
      margin-bottom: 1rem;
    }
    .btn {
      border-radius: 8px;
    }
    .btn-lg {
      border-radius: 12px;
      font-weight: 600;
    }
    
    .fab {
      position: fixed;
      bottom: 80px;
      right: 20px;
      background-color: #ffc107;
      color: #000;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 28px;
      box-shadow: 0 4px 10px rgba(0,0,0,.3);
      text-decoration: none;
      z-index: 1000;
    }
    
    @media (min-width: 768px) {
      .bottom-nav, .fab {
        display: none;
      }
      body {
        padding-bottom: 0;
      }
    }
  </style>
  {% block extra_head %}{% endblock %}
</head>
<body>

<nav class="navbar navbar-expand-md navbar-top d-none d-md-flex mb-4">
  <div class="container">
    <a class="navbar-brand" href="{% url 'eventos:dashboard' %}">
      <i class="bi bi-tent"></i> ART.TENDAS
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <a class="nav-link fw-bold {% block nav_dashboard %}{% endblock %}" href="{% url 'eventos:dashboard' %}">Início</a>
        </li>
        <li class="nav-item">
          <a class="nav-link fw-bold {% block nav_eventos %}{% endblock %}" href="{% url 'eventos:lista' %}">Eventos</a>
        </li>
        <li class="nav-item">
          <a class="nav-link fw-bold {% block nav_inventario %}{% endblock %}" href="{% url 'inventario:inventario' %}">Inventário</a>
        </li>
      </ul>
      <a href="{% url 'eventos:novo' %}" class="btn btn-dark fw-bold">+ Novo Evento</a>
    </div>
  </div>
</nav>

<div class="d-md-none navbar-top p-3 text-center sticky-top mb-3 shadow-sm">
  <h4 class="m-0 fw-bold"><i class="bi bi-tent"></i> ART.TENDAS</h4>
</div>

<div class="container pb-5">
  {% if messages %}
    {% for message in messages %}
      <div class="alert alert-{{ message.tags }} alert-dismissible fade show shadow-sm" role="alert">
        {{ message }}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    {% endfor %}
  {% endif %}

  {% block content %}{% endblock %}
</div>

<nav class="bottom-nav d-md-none">
  <a href="{% url 'eventos:dashboard' %}" class="bottom-nav-item {% block mob_dashboard %}{% endblock %}">
    <i class="bi bi-house-door-fill"></i>
    Início
  </a>
  <a href="{% url 'eventos:lista' %}" class="bottom-nav-item {% block mob_eventos %}{% endblock %}">
    <i class="bi bi-calendar-event-fill"></i>
    Eventos
  </a>
  <a href="{% url 'inventario:inventario' %}" class="bottom-nav-item {% block mob_inventario %}{% endblock %}">
    <i class="bi bi-box-seam-fill"></i>
    Estoque
  </a>
</nav>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
{% block extra_scripts %}{% endblock %}
</body>
</html>
"""

dashboard_html = """{% extends 'base.html' %}
{% load static %}
{% block title %}Início{% endblock %}
{% block nav_dashboard %}active{% endblock %}
{% block mob_dashboard %}active{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <div>
    <h3 class="fw-bold mb-0">Dashboard</h3>
    <span class="text-muted small">Resumo da operação</span>
  </div>
</div>

<div class="row g-2 mb-4">
  <div class="col-6">
    <div class="card h-100 bg-white border border-primary border-2 text-center p-3 shadow-sm">
      <h2 class="fw-bold text-primary mb-0">{{ ativos }}</h2>
      <small class="text-muted fw-bold">Eventos Ativos</small>
    </div>
  </div>
  <div class="col-6">
    <div class="card h-100 bg-warning text-dark text-center p-3 shadow-sm border-0">
      <h2 class="fw-bold mb-0">{{ tendas_em_uso }}</h2>
      <small class="fw-bold">Tendas em Uso</small>
    </div>
  </div>
</div>

<h5 class="fw-bold mb-3 mt-2 text-secondary">Eventos da Semana</h5>
{% if proximos %}
  <div class="row g-3 mb-4">
    {% for evento in proximos %}
      <div class="col-12 col-md-6">
        <div class="card p-3 border-start border-5 border-warning shadow-sm">
          <div class="d-flex justify-content-between">
            <h5 class="fw-bold mb-1 text-truncate" style="max-width: 70%;">{{ evento.nome }}</h5>
            <span class="badge bg-warning text-dark rounded-pill align-self-start">{{ evento.data_inicio|date:"d/m" }}</span>
          </div>
          <p class="text-muted small mb-1"><i class="bi bi-person-fill"></i> {{ evento.cliente }}</p>
          <p class="text-muted small mb-3"><i class="bi bi-geo-alt-fill"></i> {{ evento.cidade }}</p>
          <div class="d-flex justify-content-between align-items-center">
            <small class="text-secondary fw-bold">⛺ {{ evento.total_tendas }} | 🎪 {{ evento.total_placas }}</small>
            <a href="{% url 'eventos:detalhe' evento.pk %}" class="btn btn-sm btn-dark px-3 fw-bold rounded-pill">Ver</a>
          </div>
        </div>
      </div>
    {% endfor %}
  </div>
{% else %}
  <div class="card p-4 text-center text-muted mb-4 border-0 bg-light shadow-sm">
    <i class="bi bi-calendar-check fs-1 mb-2"></i>
    <p class="mb-0">Sem eventos agendados próximos.</p>
  </div>
{% endif %}

<h5 class="fw-bold mb-3 text-secondary">Mapa de Montagem</h5>
<div class="card overflow-hidden shadow-sm border-0 mb-4">
  <div id="map" style="height: 250px; width: 100%;"></div>
</div>

<a href="{% url 'eventos:novo' %}" class="fab">
  <i class="bi bi-plus"></i>
</a>
{% endblock %}

{% block extra_scripts %}
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
document.addEventListener("DOMContentLoaded", function() {
  const mapEl = document.getElementById('map');
  if (!mapEl) return;
  const eventosData = {{ eventos_mapa_json|safe }};
  const map = L.map('map').setView([-15.5362, -47.3344], 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
  }).addTo(map);

  if (eventosData.length > 0) {
    const bounds = [];
    eventosData.forEach(ev => {
      const marker = L.marker([ev.lat, ev.lng]).addTo(map);
      marker.bindPopup(`<b>${ev.nome}</b><br>${ev.cliente}<br><a href="${ev.url}">Detalhes</a>`);
      bounds.push([ev.lat, ev.lng]);
    });
    map.fitBounds(bounds, {padding: [20, 20]});
  }
});
</script>
{% endblock %}
"""

lista_eventos_html = """{% extends 'base.html' %}
{% block title %}Eventos{% endblock %}
{% block nav_eventos %}active{% endblock %}
{% block mob_eventos %}active{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h3 class="fw-bold mb-0">Eventos</h3>
  <a href="{% url 'eventos:novo' %}" class="btn btn-warning fw-bold d-none d-md-inline-block">+ Novo</a>
</div>

<form method="get" class="mb-4">
  <div class="input-group shadow-sm">
    <input type="text" name="q" class="form-control form-control-lg border-0" placeholder="Buscar por cliente, local..." value="{{ q }}">
    <button class="btn btn-warning border-0 px-4" type="submit"><i class="bi bi-search"></i></button>
  </div>
</form>

{% if eventos %}
  <div class="row g-3">
    {% for evento in eventos %}
      <div class="col-12 col-md-6 col-lg-4">
        <div class="card p-3 shadow-sm h-100">
          <div class="d-flex justify-content-between align-items-start mb-2">
            <h5 class="fw-bold text-truncate mb-0" style="max-width: 75%;">{{ evento.nome }}</h5>
            {% if evento.status == 'agendado' %}
              <span class="badge bg-primary rounded-pill">Agendado</span>
            {% elif evento.status == 'em_andamento' %}
              <span class="badge bg-warning text-dark rounded-pill">Andamento</span>
            {% elif evento.status == 'concluido' %}
              <span class="badge bg-success rounded-pill">Concluído</span>
            {% else %}
              <span class="badge bg-secondary rounded-pill">Cancelado</span>
            {% endif %}
          </div>
          <p class="small text-muted mb-1"><i class="bi bi-person"></i> {{ evento.cliente }}</p>
          <p class="small text-muted mb-2"><i class="bi bi-calendar"></i> {{ evento.data_inicio|date:"d/m/y" }} a {{ evento.data_fim|date:"d/m/y" }}</p>
          <div class="mt-auto pt-2 border-top text-end">
            <a href="{% url 'eventos:detalhe' evento.pk %}" class="btn btn-outline-dark btn-sm rounded-pill px-3 fw-bold w-100">Ver Evento</a>
          </div>
        </div>
      </div>
    {% endfor %}
  </div>
{% else %}
  <div class="text-center p-5 text-muted">
    <i class="bi bi-search fs-1 mb-3"></i>
    <p>Nenhum evento encontrado.</p>
  </div>
{% endif %}

<a href="{% url 'eventos:novo' %}" class="fab">
  <i class="bi bi-plus"></i>
</a>
{% endblock %}
"""

detalhe_evento_html = """{% extends 'base.html' %}
{% block title %}Detalhe: {{ evento.nome }}{% endblock %}
{% block nav_eventos %}active{% endblock %}
{% block mob_eventos %}active{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <a href="{% url 'eventos:lista' %}" class="btn btn-outline-secondary btn-sm rounded-pill"><i class="bi bi-arrow-left"></i> Voltar</a>
  <div class="dropdown">
    <button class="btn btn-light rounded-circle" type="button" data-bs-toggle="dropdown">
      <i class="bi bi-three-dots-vertical"></i>
    </button>
    <ul class="dropdown-menu dropdown-menu-end shadow border-0">
      <li><a class="dropdown-item fw-bold" href="{% url 'eventos:editar' evento.pk %}"><i class="bi bi-pencil me-2"></i> Editar</a></li>
      <li><hr class="dropdown-divider"></li>
      <li><a class="dropdown-item text-danger fw-bold" href="{% url 'eventos:excluir' evento.pk %}"><i class="bi bi-trash me-2"></i> Excluir</a></li>
    </ul>
  </div>
</div>

<div class="card shadow-sm p-4 mb-4 border-top border-warning border-5">
  <h2 class="fw-bold mb-1">{{ evento.nome }}</h2>
  <div class="mb-3">
    {% if evento.status == 'agendado' %}
      <span class="badge bg-primary px-3 py-2 rounded-pill">Agendado</span>
    {% elif evento.status == 'em_andamento' %}
      <span class="badge bg-warning text-dark px-3 py-2 rounded-pill">Em Andamento</span>
    {% elif evento.status == 'concluido' %}
      <span class="badge bg-success px-3 py-2 rounded-pill">Concluído</span>
    {% else %}
      <span class="badge bg-secondary px-3 py-2 rounded-pill">Cancelado</span>
    {% endif %}
  </div>
  
  <ul class="list-group list-group-flush mb-0">
    <li class="list-group-item bg-transparent px-0 py-3">
      <small class="text-muted d-block text-uppercase fw-bold">Cliente / Responsável</small>
      <span class="fs-5">{{ evento.cliente }}</span>
      {% if evento.telefone %}
        <br><a href="tel:{{ evento.telefone }}" class="btn btn-sm btn-outline-success mt-2 rounded-pill"><i class="bi bi-whatsapp"></i> {{ evento.telefone }}</a>
      {% endif %}
    </li>
    <li class="list-group-item bg-transparent px-0 py-3">
      <small class="text-muted d-block text-uppercase fw-bold">Datas</small>
      <span class="fs-5">{{ evento.data_inicio|date:"d/m/Y" }} até {{ evento.data_fim|date:"d/m/Y" }}</span>
    </li>
    <li class="list-group-item bg-transparent px-0 py-3">
      <small class="text-muted d-block text-uppercase fw-bold">Local</small>
      <span>{{ evento.local }} - {{ evento.cidade }}</span>
    </li>
    {% if evento.observacoes %}
    <li class="list-group-item bg-transparent px-0 py-3">
      <small class="text-muted d-block text-uppercase fw-bold">Observações</small>
      <p class="mb-0">{{ evento.observacoes }}</p>
    </li>
    {% endif %}
  </ul>
</div>

<div class="row g-4 mb-5">
  <div class="col-12 col-md-6">
    <div class="card shadow-sm h-100 p-3">
      <h5 class="fw-bold mb-3"><i class="bi bi-tent"></i> Tendas Alocadas</h5>
      {% if evento.tendas.all %}
        <ul class="list-group list-group-flush">
          {% for t in evento.tendas.all %}
            <li class="list-group-item px-0 d-flex justify-content-between align-items-center">
              <span>{{ t.codigo }} - {{ t.get_tamanho_display }}</span>
              <span class="badge bg-light text-dark border">{{ t.get_tipo_display }}</span>
            </li>
          {% endfor %}
        </ul>
      {% else %}
        <p class="text-muted small">Nenhuma tenda alocada.</p>
      {% endif %}
    </div>
  </div>
  
  <div class="col-12 col-md-6">
    <div class="card shadow-sm h-100 p-3">
      <h5 class="fw-bold mb-3"><i class="bi bi-box"></i> Palco / Piso</h5>
      {% if evento.conjuntos.all %}
        <ul class="list-group list-group-flush">
          {% for c in evento.conjuntos.all %}
            <li class="list-group-item px-0 d-flex justify-content-between align-items-center">
              <span>{{ c.nome }}</span>
              <span class="badge bg-secondary rounded-pill">{{ c.quantidade_placas }} placas</span>
            </li>
          {% endfor %}
        </ul>
      {% else %}
        <p class="text-muted small">Nenhum conjunto alocado.</p>
      {% endif %}
    </div>
  </div>
</div>
{% endblock %}
"""

form_evento_html = """{% extends 'base.html' %}
{% block title %}{{ titulo }}{% endblock %}

{% block content %}
<div class="d-flex align-items-center mb-4">
  <a href="javascript:history.back()" class="btn btn-light rounded-circle me-3"><i class="bi bi-arrow-left"></i></a>
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

    <h5 class="fw-bold mb-3 text-secondary border-bottom pb-2">Informações Gerais</h5>
    
    <div class="mb-3">
      <label class="form-label fw-bold">Nome do Evento</label>
      {{ form.nome }}
    </div>
    
    <div class="mb-3">
      <label class="form-label fw-bold">Cliente / Responsável</label>
      {{ form.cliente }}
    </div>
    
    <div class="mb-3">
      <label class="form-label fw-bold">Telefone (Opcional)</label>
      {{ form.telefone }}
    </div>

    <div class="row g-3 mb-4">
      <div class="col-6">
        <label class="form-label fw-bold">Data Início</label>
        {{ form.data_inicio }}
      </div>
      <div class="col-6">
        <label class="form-label fw-bold">Data Fim</label>
        {{ form.data_fim }}
      </div>
    </div>
    
    <h5 class="fw-bold mb-3 text-secondary border-bottom pb-2 mt-4">Localização</h5>
    <div class="mb-3">
      <label class="form-label fw-bold">Endereço / Local</label>
      {{ form.local }}
    </div>
    <div class="mb-3">
      <label class="form-label fw-bold">Cidade</label>
      {{ form.cidade }}
    </div>
    
    <div class="row g-3 mb-4">
      <div class="col-6">
        <label class="form-label fw-bold">Latitude (Opcional)</label>
        {{ form.latitude }}
      </div>
      <div class="col-6">
        <label class="form-label fw-bold">Longitude (Opcional)</label>
        {{ form.longitude }}
      </div>
    </div>

    <h5 class="fw-bold mb-3 text-secondary border-bottom pb-2 mt-4">Status & Obs</h5>
    <div class="mb-3">
      <label class="form-label fw-bold">Status do Evento</label>
      {{ form.status }}
    </div>
    <div class="mb-4">
      <label class="form-label fw-bold">Observações</label>
      {{ form.observacoes }}
    </div>

    <h5 class="fw-bold mb-3 text-secondary border-bottom pb-2 mt-4">Alocação de Equipamentos</h5>
    <div class="mb-4">
      <label class="form-label fw-bold d-block"><i class="bi bi-tent"></i> Selecionar Tendas</label>
      <div class="bg-light p-3 rounded" style="max-height: 250px; overflow-y: auto;">
        {{ form.tendas }}
      </div>
    </div>
    
    <div class="mb-4">
      <label class="form-label fw-bold d-block"><i class="bi bi-box"></i> Selecionar Conjuntos</label>
      <div class="bg-light p-3 rounded" style="max-height: 250px; overflow-y: auto;">
        {{ form.conjuntos }}
      </div>
    </div>

    <div class="d-grid mt-5">
      <button type="submit" class="btn btn-warning btn-lg shadow">SALVAR EVENTO</button>
    </div>
  </form>
</div>
{% endblock %}
"""

inventario_html = """{% extends 'base.html' %}
{% block title %}Inventário{% endblock %}
{% block nav_inventario %}active{% endblock %}
{% block mob_inventario %}active{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
  <h3 class="fw-bold mb-0">Estoque</h3>
  <div class="dropdown d-none d-md-block">
    <button class="btn btn-warning fw-bold dropdown-toggle" type="button" data-bs-toggle="dropdown">
      + Novo Item
    </button>
    <ul class="dropdown-menu">
      <li><a class="dropdown-item fw-bold" href="{% url 'inventario:nova_tenda' %}"><i class="bi bi-tent"></i> Nova Tenda</a></li>
      <li><a class="dropdown-item fw-bold" href="{% url 'inventario:novo_conjunto' %}"><i class="bi bi-box"></i> Novo Conjunto</a></li>
    </ul>
  </div>
</div>

<ul class="nav nav-pills nav-fill mb-4 p-1 bg-white rounded-pill shadow-sm" id="pills-tab" role="tablist">
  <li class="nav-item" role="presentation">
    <button class="nav-link active rounded-pill fw-bold" data-bs-toggle="pill" data-bs-target="#tendas" type="button">Tendas</button>
  </li>
  <li class="nav-item" role="presentation">
    <button class="nav-link rounded-pill fw-bold" data-bs-toggle="pill" data-bs-target="#palcos" type="button">Palcos/Pisos</button>
  </li>
</ul>

<div class="tab-content" id="pills-tabContent">
  <!-- TENDAS TAB -->
  <div class="tab-pane fade show active" id="tendas" role="tabpanel">
    <div class="row g-3">
      {% for tenda in tendas %}
        <div class="col-12 col-md-6 col-lg-4">
          <div class="card p-3 shadow-sm h-100 border-start border-4 
            {% if tenda.status == 'disponivel' %}border-success{% elif tenda.status == 'em_uso' %}border-warning{% else %}border-danger{% endif %}">
            
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h5 class="fw-bold mb-0">{{ tenda.codigo }}</h5>
              <a href="{% url 'inventario:editar_tenda' tenda.pk %}" class="btn btn-sm btn-light rounded-circle"><i class="bi bi-pencil"></i></a>
            </div>
            
            <p class="mb-1 text-muted"><i class="bi bi-arrows-fullscreen"></i> {{ tenda.get_tamanho_display }}</p>
            <p class="mb-2 text-muted"><i class="bi bi-tags"></i> {{ tenda.get_tipo_display }}</p>
            
            <div class="mt-auto">
              {% if tenda.status == 'disponivel' %}
                <span class="badge bg-success w-100 py-2">Disponível</span>
              {% elif tenda.status == 'em_uso' %}
                <span class="badge bg-warning text-dark w-100 py-2">Em Uso</span>
              {% else %}
                <span class="badge bg-danger w-100 py-2">Manutenção</span>
              {% endif %}
            </div>
          </div>
        </div>
      {% empty %}
        <div class="col-12 text-center py-5 text-muted">
          <i class="bi bi-box-seam fs-1 mb-2"></i>
          <p>Nenhuma tenda cadastrada no inventário.</p>
        </div>
      {% endfor %}
    </div>
  </div>

  <!-- PALCOS TAB -->
  <div class="tab-pane fade" id="palcos" role="tabpanel">
    <div class="row g-3">
      {% for c in conjuntos %}
        <div class="col-12 col-md-6 col-lg-4">
          <div class="card p-3 shadow-sm h-100 border-start border-4 
            {% if c.status == 'disponivel' %}border-success{% elif c.status == 'em_uso' %}border-warning{% else %}border-danger{% endif %}">
            
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h5 class="fw-bold mb-0">{{ c.nome }}</h5>
              <a href="{% url 'inventario:editar_conjunto' c.pk %}" class="btn btn-sm btn-light rounded-circle"><i class="bi bi-pencil"></i></a>
            </div>
            
            <h2 class="fw-bold text-center my-3">{{ c.quantidade_placas }} <span class="fs-6 text-muted fw-normal">placas</span></h2>
            
            <div class="mt-auto">
              {% if c.status == 'disponivel' %}
                <span class="badge bg-success w-100 py-2">Disponível</span>
              {% elif c.status == 'em_uso' %}
                <span class="badge bg-warning text-dark w-100 py-2">Em Uso</span>
              {% else %}
                <span class="badge bg-danger w-100 py-2">Manutenção</span>
              {% endif %}
            </div>
          </div>
        </div>
      {% empty %}
        <div class="col-12 text-center py-5 text-muted">
          <i class="bi bi-grid-3x3 fs-1 mb-2"></i>
          <p>Nenhum conjunto cadastrado.</p>
        </div>
      {% endfor %}
    </div>
  </div>
</div>

<!-- Modal Bottom Sheet / Dropup menu for mobile Fab -->
<div class="dropdown d-md-none">
  <button class="fab" type="button" data-bs-toggle="dropdown" aria-expanded="false">
    <i class="bi bi-plus"></i>
  </button>
  <ul class="dropdown-menu dropdown-menu-end shadow border-0 mb-2 p-2">
    <li><a class="dropdown-item py-2 fw-bold" href="{% url 'inventario:nova_tenda' %}"><i class="bi bi-tent me-2 text-warning"></i> Nova Tenda</a></li>
    <li><a class="dropdown-item py-2 fw-bold" href="{% url 'inventario:novo_conjunto' %}"><i class="bi bi-box me-2 text-warning"></i> Novo Conjunto</a></li>
  </ul>
</div>
{% endblock %}
"""

import os
def write_tpl(path, content):
    with open(os.path.join(templates_dir, path), "w", encoding="utf-8") as f:
        f.write(content)

write_tpl("base.html", base_html)
write_tpl(r"eventos\dashboard.html", dashboard_html)
write_tpl(r"eventos\lista.html", lista_eventos_html)
write_tpl(r"eventos\detalhe.html", detalhe_evento_html)
write_tpl(r"eventos\form_evento.html", form_evento_html)
write_tpl(r"inventario\inventario.html", inventario_html)

print("Templates reescritos com sucesso!")
