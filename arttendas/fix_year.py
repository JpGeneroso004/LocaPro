import os

for path in ['templates/base.html', 'templates/landing.html']:
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('2026', '{% now "Y" %}')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
print('Done.')
