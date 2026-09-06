
import os
with open("inventario/views.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace excluir_tenda
old_tenda = """        em_uso = tenda.eventos.filter(status__in=['agendado', 'em_andamento']).exists()
        if em_uso:
            messages.error(request, f'Erro: A Tenda {tenda.codigo} não pode ser excluída pois está reservada ou em uso em um evento ativo.')
        else:
            cod = tenda.codigo
            tenda.delete()
            messages.success(request, f'Tenda {cod} removida com sucesso!')"""

new_tenda = """        em_uso = tenda.eventos.filter(status__in=['agendado', 'em_andamento']).exists()
        if em_uso:
            messages.error(request, f'Erro: A Tenda {tenda.codigo} não pode ser excluída pois está reservada ou em uso em um evento ativo.')
        else:
            # Soft Delete if it has historical events
            if tenda.eventos.exists():
                tenda.status = "baixado"
                tenda.save()
                messages.warning(request, f'A Tenda {tenda.codigo} possui histórico de eventos passados e foi movida para Descartada/Vendida (para auditoria) ao invés de apagada.')
            else:
                cod = tenda.codigo
                tenda.delete()
                messages.success(request, f'Tenda {cod} removida permanentemente com sucesso!')"""

text = text.replace(old_tenda, new_tenda)

old_conjunto = """        em_uso = conjunto.eventos.filter(status__in=['agendado', 'em_andamento']).exists()
        if em_uso:
            messages.error(request, f'Erro: O Conjunto "{conjunto.nome}" não pode ser excluído pois está reservado ou em uso em um evento ativo.')
        else:
            nome = conjunto.nome
            conjunto.delete()
            messages.success(request, f'Conjunto "{nome}" removido com sucesso!')"""

new_conjunto = """        em_uso = conjunto.eventos.filter(status__in=['agendado', 'em_andamento']).exists()
        if em_uso:
            messages.error(request, f'Erro: O Conjunto "{conjunto.nome}" não pode ser excluído pois está reservado ou em uso em um evento ativo.')
        else:
            if conjunto.eventos.exists():
                conjunto.status = "baixado"
                conjunto.save()
                messages.warning(request, f'O Conjunto "{conjunto.nome}" possui histórico de eventos passados e foi movido para Descartado/Vendido (para auditoria).')
            else:
                nome = conjunto.nome
                conjunto.delete()
                messages.success(request, f'Conjunto "{nome}" removido permanentemente com sucesso!')"""

text = text.replace(old_conjunto, new_conjunto)

with open("inventario/views.py", "w", encoding="utf-8") as f:
    f.write(text)
print("Done")

