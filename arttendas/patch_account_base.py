import os

base_path = 'templates/account/base.html'
with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

back_button = '''
  <script>
    function smartBack() {
      if (document.referrer && document.referrer.includes(window.location.host)) {
        window.history.back();
      } else {
        window.location.href = "/";
      }
    }
  </script>
  <div class="auth-card">
    <a href="javascript:void(0)" onclick="smartBack()" style="text-decoration:none; color:#666; font-weight:bold; display:inline-block; margin-bottom: 20px;">
      &larr; Voltar
    </a>
'''

if '&larr; Voltar' not in content:
    content = content.replace('<div class="auth-card">', back_button)
    with open(base_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Added back button to account/base.html')
