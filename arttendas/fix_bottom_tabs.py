import os
import re

file_path = 'templates/base.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for href before class
pattern = r'href="\{%\s*url\s*\'([^\']+)\'\s*%\}"[^>]*?class="([^"]+)"'

def inject_active_reverse(match):
    full_str = match.group(0)
    url_name = match.group(1)   
    class_attr = match.group(2) 
    
    # avoid double injecting
    if 'request.resolver_match' in class_attr:
        return full_str
        
    new_class = f'class="{class_attr} {{% if request.resolver_match.view_name == \'{url_name}\' %}}active fw-bolder{{% endif %}}"'
    return full_str.replace(f'class="{class_attr}"', new_class)

content = re.sub(pattern, inject_active_reverse, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated bottom-nav-item in base.html')
