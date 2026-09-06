import os

for path in ['empresas/tests.py', 'eventos/tests.py', 'inventario/tests.py']:
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('nome_fantasia=', 'nome=')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
print('Tests updated.')
