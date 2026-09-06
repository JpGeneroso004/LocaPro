import os
import re

file_path = 'eventos/views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir o trecho de novo_evento
novo_evento_regex = re.compile(r'def novo_evento\(request\):.*?return render\(request, \'eventos/form_evento\.html\', \{.*?\}\)', re.DOTALL)

novo_evento_replacement = '''def novo_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        itens_str = request.POST.get('itens_json', '[]')
        
        import json
        itens = []
        try:
            itens = json.loads(itens_str)
        except Exception:
            pass
            
        if not itens:
            form.add_error(None, 'Você precisa adicionar pelo menos um equipamento ao evento.')
            
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizacao = request.user.organizacao
            evento.save()
            
            for item in itens:
                eq_id = item.get('id')
                qtd = int(item.get('qtd', 1))
                try:
                    eq = Equipamento.objects.get(id=eq_id, organizacao=request.user.organizacao)
                    ItemEvento.objects.create(
                        evento=evento,
                        equipamento=eq,
                        quantidade=qtd,
                        preco_fechado=eq.valor_diaria * qtd
                    )
                except Equipamento.DoesNotExist:
                    pass
            
            messages.success(request, 'Evento cadastrado com sucesso!')
            return redirect('eventos:detalhe', pk=evento.pk)
        else:
            messages.error(request, 'Erro ao criar evento. Verifique os campos.')
    else:
        form = EventoForm()
    return render(request, 'eventos/form_evento.html', {'form': form, 'titulo': 'Novo Evento'})'''

content = novo_evento_regex.sub(novo_evento_replacement, content, count=1)

# Agora para editar_evento
editar_evento_regex = re.compile(r'def editar_evento\(request, pk\):.*?return render\(request, \'eventos/form_evento\.html\', \{.*?\}\)', re.DOTALL)

editar_evento_replacement = '''def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        itens_str = request.POST.get('itens_json', '[]')
        
        import json
        itens = []
        try:
            itens = json.loads(itens_str)
        except Exception:
            pass
            
        if not itens:
            form.add_error(None, 'Você precisa ter pelo menos um equipamento no evento.')
            
        if form.is_valid():
            form.save()
            
            evento.itens.all().delete()
            for item in itens:
                eq_id = item.get('id')
                qtd = int(item.get('qtd', 1))
                try:
                    eq = Equipamento.objects.get(id=eq_id, organizacao=request.user.organizacao)
                    ItemEvento.objects.create(
                        evento=evento,
                        equipamento=eq,
                        quantidade=qtd,
                        preco_fechado=eq.valor_diaria * qtd
                    )
                except Equipamento.DoesNotExist:
                    pass
            
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('eventos:detalhe', pk=evento.pk)
        else:
            messages.error(request, 'Erro ao atualizar evento. Verifique os campos.')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/form_evento.html', {'form': form, 'evento': evento, 'titulo': 'Editar Evento'})'''

content = editar_evento_regex.sub(editar_evento_replacement, content, count=1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated views.py')
