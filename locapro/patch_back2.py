import os

base_path = 'templates/base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    base_content = f.read()

back_button = '''
        <!-- Smart Back Button (Visible when not on Dashboard) -->
        {% if request.resolver_match.view_name != 'eventos:dashboard' and request.resolver_match.view_name != 'home' %}
        <a href="javascript:void(0)" onclick="smartBack()" class="btn btn-link text-body p-0 me-3 text-decoration-none" title="Voltar">
          <i class="bi bi-arrow-left fs-2"></i>
        </a>
        {% endif %}
        <a class="navbar-brand d-flex align-items-center m-0'''

base_content = base_content.replace('<a class="navbar-brand d-flex align-items-center m-0', back_button)

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(base_content)

print('Patched base.html again.')
