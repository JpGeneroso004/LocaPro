import os

# 1. Patch base.html
base_path = 'templates/base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    base_content = f.read()

back_button = '''
      <div class="d-flex align-items-center">
        <!-- Smart Back Button (Visible when not on Dashboard) -->
        {% if request.resolver_match.view_name != 'eventos:dashboard' and request.resolver_match.view_name != 'home' %}
        <a href="javascript:void(0)" onclick="smartBack()" class="btn btn-link text-body p-0 me-3 text-decoration-none" title="Voltar">
          <i class="bi bi-arrow-left fs-2"></i>
        </a>
        {% endif %}
        
        <a class="navbar-brand d-flex align-items-center m-0" href="{% url 'eventos:dashboard' %}">
'''
base_content = base_content.replace('<div class="d-flex align-items-center">\n        {% if user.is_authenticated %}', back_button + '        {% if user.is_authenticated %}')
base_content = base_content.replace('<div class="d-flex align-items-center">\n        <a href="{% url \'account_logout\' %}"', back_button + '        <a href="{% url \'account_logout\' %}"')

js_script = '''
  <script>
    function smartBack() {
      if (document.referrer && document.referrer.includes(window.location.host)) {
        window.history.back();
      } else {
        window.location.href = "{% url 'eventos:dashboard' %}";
      }
    }
'''
base_content = base_content.replace('<script>', js_script, 1)

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(base_content)


# 2. Patch account/login.html and cadastro.html
for path in ['templates/account/login.html', 'empresas/templates/empresas/cadastro.html']:
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    back_btn = '''
        <div class="mb-4">
          <a href="javascript:void(0)" onclick="smartBack()" class="btn btn-outline-secondary rounded-pill px-4 btn-sm fw-bold">
            <i class="bi bi-arrow-left"></i> Voltar
          </a>
        </div>
'''
    if '<div class="form-container">' in content:
        content = content.replace('<div class="form-container">', '<div class="form-container">' + back_btn)
    
    if '</body>' in content:
        content = content.replace('</body>', '''
<script>
  function smartBack() {
    if (document.referrer && document.referrer.includes(window.location.host)) {
      window.history.back();
    } else {
      window.location.href = "/";
    }
  }
</script>
</body>''')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Patched base, login, and cadastro with Smart Back Button.')
