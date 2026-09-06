import os

for path in ['empresas/tests.py', 'eventos/tests.py', 'inventario/tests.py']:
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('email="alpha@teste.com",', 'username="alpha", email="alpha@teste.com",')
    content = content.replace('email="beta@teste.com",', 'username="beta", email="beta@teste.com",')
    content = content.replace('email="alpha@test.com",', 'username="alpha2", email="alpha@test.com",')
    content = content.replace('email="beta@test.com",', 'username="beta2", email="beta@test.com",')
    content = content.replace('email="test@org.com",', 'username="testuser", email="test@org.com",')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
