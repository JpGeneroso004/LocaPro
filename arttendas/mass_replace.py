import os

def replace_in_file(filepath, old, new):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

# Login / Cadastro
replace_in_file('templates/registration/login.html', 'text-dark mb-1', 'text-body mb-1')
replace_in_file('empresas/templates/empresas/cadastro.html', 'text-dark mb-1', 'text-body mb-1')

# Dashboard
replace_in_file('templates/eventos/dashboard.html', 'fw-bold text-dark mb-0', 'fw-bold text-body mb-0')
replace_in_file('templates/eventos/dashboard.html', 'fw-bold text-dark\">Bem-vindo', 'fw-bold text-body\">Bem-vindo')

# Financeiro
replace_in_file('empresas/templates/empresas/financeiro.html', 'bg-white', 'bg-transparent')
replace_in_file('empresas/templates/empresas/financeiro.html', 'fw-bold text-dark', 'fw-bold text-body')
# Revert bg-warning text-dark changes in Financeiro that might have been hit
replace_in_file('empresas/templates/empresas/financeiro.html', 'bg-warning text-body', 'bg-warning text-dark')

# Pagination in lists
for filepath in ['templates/eventos/lista.html', 'templates/eventos/contratos_lista.html']:
    replace_in_file(filepath, 'page-link text-dark', 'page-link text-body')

print('Substituições concluídas.')
