import os

file_path = 'empresas/templates/empresas/assinatura.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('card-header py-4 bg-light border-bottom-0', 'card-header py-4 bg-body-tertiary border-bottom-0')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated Essencial card background.')
