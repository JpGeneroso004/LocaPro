import os
import re

file_path = 'templates/base.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# First, remove old {% block nav_X %}{% endblock %} to clean it up
content = re.sub(r'\{% block nav_[a-z_]+ %\}\{% endblock %\}', '', content)
content = re.sub(r'\{% block mob_[a-z_]+ %\}\{% endblock %\}', '', content)

# Now inject active classes based on url tag
def inject_active(match):
    # match.group(0) is the full match: class="nav-link fs-5" href="{% url 'namespace:view' %}"
    # We want to insert {% if request.resolver_match.view_name == 'namespace:view' %}active{% endif %} inside the class string
    full_str = match.group(0)
    class_attr = match.group(1) # nav-link fs-5
    url_name = match.group(2)   # namespace:view
    
    # We reconstruct the class
    # If the URL is already active, we make it 'active'. If it's the bottom nav, 'active text-primary' looks better but 'active' alone is standard bootstrap
    new_class = f'class="{class_attr} {{% if request.resolver_match.view_name == \'{url_name}\' %}}active fw-bolder{{% endif %}}"'
    return full_str.replace(f'class="{class_attr}"', new_class)

# Matches <a class="..." href="{% url 'something' %}">
# We use regex to find class="..." and href="{% url '...' %}"
pattern = r'class="([^"]+)"[^>]*?href="\{%\s*url\s*\'([^\']+)\'\s*%\}"'

content = re.sub(pattern, inject_active, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated base.html')
