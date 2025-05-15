from django.urls import path
from . import views

urlpatterns = [
    path('lista_publicaciones/', views.lista_publicaciones, name='lista_publicaciones'),
    path('crear_publicacion/', views.crear_publicacion, name='crear_publicacion'),
    path('publicacion/<int:pk>', views.detalle_publicacion, name='detalle_publicacion'),
    path('publicacion/<int:pk>/comentar/', views.agregar_comentario, name='agregar_comentario'),
]