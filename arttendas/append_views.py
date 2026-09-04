import sys

content = """
def contratos_lista(request):
    from .models import Contrato
    contratos = Contrato.objects.all().order_by('-criado_em')
    return render(request, 'eventos/contratos_lista.html', {'contratos': contratos})

def gerar_contrato(request, evento_id):
    from .models import Contrato
    evento = get_object_or_404(Evento, pk=evento_id)
    if hasattr(evento, 'contrato'):
        return redirect('eventos:editar_contrato', contrato_id=evento.contrato.id)

    contratante_nome = evento.cliente
    contratante_telefone = evento.telefone
    endereco_montagem = f"{evento.rua}, {evento.numero} - {evento.setor}"
    if evento.complemento:
        endereco_montagem += f" - {evento.complemento}"
    endereco_montagem += f" - {evento.cidade}"
    
    itens = []
    if evento.tendas.exists():
        for t in evento.tendas.all():
            itens.append(f"Tenda {t.tamanho} ({t.tipo})")
    if evento.conjuntos.exists():
        for c in evento.conjuntos.all():
            itens.append(f"Conjunto {c.nome} ({c.quantidade_placas} placas de 1x1m)")
    itens_locados = "\\n".join(itens) if itens else "Nenhum item especificado."
    
    clausulas_padrao = \"\"\"1. RESPONSABILIDADE DO LOCAL: O Contratante é o único responsável por autorizações e alvarás junto a órgãos públicos (prefeitura, trânsito/tráfego, polícia) para interdição de via pública e realização do evento.
2. FORÇA MAIOR / CONDIÇÕES CLIMÁTICAS: A Contratada isenta-se de culpa por vendavais extremos, tempestades ou desabamentos causados por caso fortuito, força maior ou mau uso das estruturas por terceiros.
3. ESTRUTURAS E SEGURANÇA: O Contratante assume a guarda e integridade dos materiais (tendas, palcos, pisos) durante todo o período do evento até a finalização da desmontagem.
4. INSTALAÇÕES ELÉTRICAS E DE SOM: Fica terminantemente proibida a sobrecarga das estruturas ou a fixação indevida de equipamentos pesados sem prévia autorização técnica da Contratada.\"\"\"

    context = {
        'evento': evento,
        'contratante_nome': contratante_nome,
        'contratante_telefone': contratante_telefone,
        'endereco_montagem': endereco_montagem,
        'itens_locados': itens_locados,
        'clausulas_padrao': clausulas_padrao,
    }
    return render(request, 'eventos/form_contrato.html', context)

def salvar_contrato(request, evento_id):
    from .models import Contrato
    evento = get_object_or_404(Evento, pk=evento_id)
    if request.method == 'POST':
        contrato, created = Contrato.objects.get_or_create(evento=evento)
        contrato.contratante_nome = request.POST.get('contratante_nome', '')
        contrato.contratante_cpf_cnpj = request.POST.get('contratante_cpf_cnpj', '')
        contrato.contratante_telefone = request.POST.get('contratante_telefone', '')
        contrato.contratante_endereco = request.POST.get('contratante_endereco', '')
        
        dm = request.POST.get('data_montagem')
        dd = request.POST.get('data_desmontagem')
        if dm: contrato.data_montagem = dm
        if dd: contrato.data_desmontagem = dd
        
        contrato.endereco_montagem = request.POST.get('endereco_montagem', '')
        
        # Tratar valor vazio
        v_total = request.POST.get('valor_total', '').replace(',', '.')
        sinal = request.POST.get('sinal', '').replace(',', '.')
        
        try: contrato.valor_total = float(v_total) if v_total else 0
        except ValueError: contrato.valor_total = 0
        
        try: contrato.sinal = float(sinal) if sinal else 0
        except ValueError: contrato.sinal = 0
            
        contrato.forma_pagamento = request.POST.get('forma_pagamento', '')
        contrato.itens_locados = request.POST.get('itens_locados', '')
        contrato.clausulas = request.POST.get('clausulas', '')
        contrato.save()
        messages.success(request, 'Contrato salvo com sucesso!')
        return redirect('eventos:imprimir_contrato', contrato_id=contrato.id)
    return redirect('eventos:contratos_lista')

def editar_contrato(request, contrato_id):
    from .models import Contrato
    contrato = get_object_or_404(Contrato, pk=contrato_id)
    return render(request, 'eventos/form_contrato.html', {'contrato': contrato, 'evento': contrato.evento})

def imprimir_contrato(request, contrato_id):
    from .models import Contrato
    contrato = get_object_or_404(Contrato, pk=contrato_id)
    return render(request, 'eventos/imprimir_contrato.html', {'contrato': contrato})

def deletar_contrato(request, contrato_id):
    from .models import Contrato
    contrato = get_object_or_404(Contrato, pk=contrato_id)
    if request.method == 'POST':
        contrato.delete()
        messages.success(request, 'Contrato removido.')
        return redirect('eventos:contratos_lista')
    return redirect('eventos:contratos_lista')
"""
with open(r'C:\ArtTendas\arttendas\eventos\views.py', 'a', encoding='utf-8') as f:
    f.write(content)
