from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login/', views.iniciar_sesion, name='login'),
    path('', views.iniciar_sesion, name='login'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('producto/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('producto/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('registrar/', views.registrar, name='registrar'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
