from django.contrib import admin
from django.urls import path, include
from empresas import views as empresas_views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from django.contrib.auth import logout
from core.views import landing_page

def custom_logout(request):
    logout(request)
    return redirect('/accounts/login/')

from django.http import JsonResponse
from django.db import connection

def healthcheck(request):
    try:
        connection.cursor()
        return JsonResponse({'status': 'ok', 'db': 'connected'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'details': str(e)}, status=500)

urlpatterns = [
    path('', landing_page, name='home'),
    path('api/health/', healthcheck, name='healthcheck'),
    path('admin/', admin.site.urls),
    path('eventos/', include('eventos.urls', namespace='eventos')),
    path('inventario/', include('inventario.urls', namespace='inventario')),
    path('empresas/', include('empresas.urls', namespace='empresas')),
    path('ia/', include('assistente_ia.urls', namespace='assistente_ia')),
    path('accounts/logout/', custom_logout, name='logout'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('privacidade/', empresas_views.privacidade, name='privacidade'),
    path('cookies/', empresas_views.cookies, name='cookies'),
]


# Serve estáticos e mídia sempre (inclusive com DEBUG=False, pois é uso local)
from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    path('privacidade/', empresas_views.privacidade, name='privacidade'),
    path('cookies/', empresas_views.cookies, name='cookies'),
]

