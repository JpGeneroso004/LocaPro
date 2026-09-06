file_path = 'empresas/templates/empresas/assinatura.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the achievements background so it follows Dark/Light mode correctly
content = content.replace('bg-white', 'bg-body')

# Fix text-dark inside headers so it becomes white in dark mode
content = content.replace('text-dark">LocaPro Essencial', 'text-body">LocaPro Essencial')
content = content.replace('>= 6 %}text-dark{%', '>= 6 %}text-body{%')
content = content.replace('>= 12 %}text-dark{%', '>= 12 %}text-body{%')
content = content.replace('>= 24 %}text-dark{%', '>= 24 %}text-body{%')

# Replace text-muted in the achievements descriptions with text-body-secondary to improve contrast in both modes
content = content.replace('text-muted small">Selo especial', 'text-body-secondary small">Selo especial')
content = content.replace('text-muted small"><strong>Upgrade Automático', 'text-body-secondary small"><strong>Upgrade Automático')
content = content.replace('text-muted small">Suporte técnico VIP', 'text-body-secondary small">Suporte técnico VIP')
content = content.replace('text-muted">Embaixador', 'text-body-secondary opacity-50">Embaixador')
content = content.replace('bg-light text-muted', 'bg-body-secondary text-secondary')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
