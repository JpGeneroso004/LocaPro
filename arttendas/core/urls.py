from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('/accounts/login/')

urlpatterns = [
    path('', lambda request: redirect('eventos:dashboard'), name='home'),
    path('admin/', admin.site.urls),
    path('eventos/', include('eventos.urls', namespace='eventos')),
    path('inventario/', include('inventario.urls', namespace='inventario')),
    path('empresas/', include('empresas.urls', namespace='empresas')),
    path('accounts/logout/', custom_logout, name='logout'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# Serve estáticos e mídia sempre (inclusive com DEBUG=False, pois é uso local)
from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'static'}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
