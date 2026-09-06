import os

replacements = [
    (r'arttendas\build.sh', 'cd arttendas', 'cd locapro'),
    (r'arttendas\core\settings.py', 'arttendas-local-app-key', 'locapro-local-app-key'),
    (r'arttendas\eventos\management\commands\seed_data.py', 'Art.Tendas Locações', 'LocaPro Locações'),
    (r'arttendas\iniciar.bat', 'Art.Tendas - Sistema de Gestao', 'LocaPro - Sistema de Gestao'),
    (r'arttendas\iniciar.bat', 'ART.TENDAS - Sistema de Gestao', 'LOCAPRO - Sistema de Gestao'),
    (r'arttendas\iniciar_oculto.vbs', r'C:\ArtTendas\arttendas\iniciar.bat', r'C:\ArtTendas\locapro\iniciar.bat'),
    (r'arttendas\setup.sh', 'Art.Tendas —', 'LocaPro —'),
    (r'arttendas\templates\eventos\imprimir_contrato.html', 'alt="Art.Tendas"', 'alt="LocaPro"'),
    (r'iniciar_sistema.bat', r'C:\ArtTendas\arttendas', r'C:\ArtTendas\locapro'),
    (r'README.md', '(anteriormente Art.Tendas)', ''),
    (r'README.md', 'cd arttendas', 'cd locapro'),
    (r'README.md', 'pasta rttendas', 'pasta locapro')
]

for filepath, old, new in replacements:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace(old, new)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print('Text replaced')
