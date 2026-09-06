import os
import re

file_path = 'templates/eventos/form_evento.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

error_block = '''
      {% if form.errors %}
        <div class="alert alert-danger mb-4 shadow-sm border-0">
          <h6 class="fw-bold"><i class="bi bi-exclamation-triangle-fill me-2"></i>Verifique os erros abaixo:</h6>
          <ul class="mb-0">
            {% for field in form %}
              {% for error in field.errors %}
                <li><strong>{{ field.label }}:</strong> {{ error }}</li>
              {% endfor %}
            {% endfor %}
            {% for error in form.non_field_errors %}
              <li>{{ error }}</li>
            {% endfor %}
          </ul>
        </div>
      {% endif %}
'''

# Replace old error block
content = re.sub(r'\{%\s*if\s*form.errors\s*%\}.*?\{%\s*endif\s*%\}', error_block, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated form_evento.html')
