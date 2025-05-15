from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from datetime import datetime
import pytz

def mi_vista(request):
    # ...existing code...
    la_paz_tz = pytz.timezone('America/La_Paz')
    hora_actual = datetime.now(la_paz_tz)
    context['hora_actual'] = hora_actual.strftime('%H:%M')
    # ...existing code...
    return render(request, 'tu_formulario.html', context)

def publicar(request):
    # ...existing code...
    la_paz_tz = pytz.timezone('America/La_Paz')
    if request.method == 'POST':
        fecha_creacion = datetime.now(la_paz_tz)
        # Aquí debes guardar fecha_creacion en tu modelo de publicación
        # Ejemplo:
        # nueva_publicacion = Publicacion(
        #     ...otros_campos...,
        #     fecha_creacion=fecha_creacion,
        # )
        # nueva_publicacion.save()
        pass
    return render(request, 'tu_formulario.html', context)

def editar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.method == 'POST':
        publicacion.titulo = request.POST.get('titulo')
        publicacion.contenido = request.POST.get('contenido')
        publicacion.save()
        return redirect('detalle_publicacion', pk=publicacion.pk)
    return render(request, 'editar_publicacion.html', {'publicacion': publicacion})

def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.method == 'POST':
        publicacion.delete()
        return redirect('lista_publicaciones')
    return render(request, 'eliminar_publicacion.html', {'publicacion': publicacion})

def cerrar_sesion(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'registration/logout.html')