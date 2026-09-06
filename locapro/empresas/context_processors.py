def tenant_context(request):
    if request.user.is_authenticated and hasattr(request.user, 'organizacao') and request.user.organizacao:
        return {
            'tenant': request.user.organizacao,
            'tenant_color': request.user.organizacao.cor_primaria,
        }
    return {
        'tenant': None,
        'tenant_color': '#004581', # Cor padrão de fallback
    }
