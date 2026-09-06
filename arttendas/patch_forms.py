import os

file_path = 'eventos/forms.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

clean_code = '''
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim    = cleaned_data.get('data_fim')
        
        if data_inicio and data_fim:
            if data_fim < data_inicio:
                self.add_error('data_fim', 'A data de fim nǜo pode ser anterior  data de incio.')
            
            # Limitar a duraǜo mǭxima do evento para 2 anos (730 dias)
            if (data_fim - data_inicio).days > 730:
                self.add_error('data_fim', 'A duraǜo do evento nǜo pode exceder 2 anos.')
            
            if data_inicio.year < 2000:
                self.add_error('data_inicio', 'Data invǭlida (muito antiga).')
                
            if data_fim.year > 2100:
                self.add_error('data_fim', 'Data invǭlida (muito no futuro).')
                
        return cleaned_data
'''

import re
content = re.sub(r'\s*def clean\(self\):.*?return cleaned_data', clean_code, content, flags=re.DOTALL)
content = content.replace('nǜo', 'não').replace(' data', 'à data').replace('incio', 'início').replace('duraǜo', 'duração').replace('mǭxima', 'máxima').replace('invǭlida', 'inválida')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated forms.py')
