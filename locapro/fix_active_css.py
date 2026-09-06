import os

file_path = 'templates/base.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

css_rule = '''
    .bottom-nav-item.active {
      color: var(--bs-warning) !important;
      font-weight: 900 !important;
    }
    
    .nav-link.active {
      color: var(--bs-warning) !important;
      font-weight: 900 !important;
      border-bottom: 2px solid var(--bs-warning);
    }
'''

content = content.replace('.bottom-nav-item.active {\n      color: var(--bs-warning);\n      font-weight: 600;\n    }', css_rule)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated CSS in base.html')
