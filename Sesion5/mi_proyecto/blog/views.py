# Vista para editar comentario
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.middleware.csrf import CsrfViewMiddleware
from .models import Publicacion, Comentario
from .forms import PublicacionForm, ComentarioForm

@login_required
@csrf_protect
def editar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    if request.user != comentario.usuario:
        return HttpResponseForbidden("no puedes editar este comentario")

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('detalle_publicacion', pk=comentario.publicacion.pk)
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, 'blog/editar_comentario.html', {'form': form})

# Create your views here.
def lista_publicaciones(request):
    publicaciones = Publicacion.objects.all()  # select * from publicacion
    return render(request,'blog/lista_publicaciones.html', {'publicaciones':publicaciones})

@csrf_protect
def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.usuario = request.user
            publicacion.save()
            return redirect('blog/home')
    else:
        form = PublicacionForm()
    return render(request,'blog/crear_publicacion.html',{'form':form})

def detalle_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion,pk=pk)
    comentarios = Comentario.objects.filter(publicacion = publicacion)
    form_comentario = ComentarioForm() if request.user.is_authenticated else None
    contexto ={
        'publicacion':publicacion,
        'comentarios':comentarios,
        'form_comentario':form_comentario,
    }
    return render(request, 'blog/detalle_publicacion.html',contexto)

@csrf_protect
def agregar_comentario(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.publicacion = publicacion
            comentario.save()
            return redirect('detalle_publicacion', pk=pk)
        else:
            # Si el formulario no es válido, renderiza con errores
            comentarios = Comentario.objects.filter(publicacion=publicacion)
            contexto = {
                'publicacion': publicacion,
                'comentarios': comentarios,
                'form_comentario': form,
            }
            return render(request, 'blog/detalle_publicacion.html', contexto)
    return HttpResponseForbidden("Método no permitido.")

@login_required
@csrf_protect
def editar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if publicacion.usuario != request.user:
        return HttpResponseForbidden("No tienes permiso para editar esta publicación.")
    if request.method == "POST":
        form = PublicacionForm(request.POST, instance=publicacion)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.usuario = request.user
            publicacion.save()
            return redirect('detalle_publicacion', pk=publicacion.pk)
    else:
        form = PublicacionForm(instance=publicacion)
    return render(request, 'blog/editar_publicacion.html', {'form': form})

@csrf_protect
def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if publicacion.usuario != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar esta publicación.")
    if request.method == "POST":
        publicacion.delete()
        return redirect('lista_publicaciones')
    # Si es GET, muestra confirmación
    return render(request, 'blog/confirmar_eliminar.html', {'publicacion': publicacion})

# Manejo global de error CSRF (opcional, para mensajes personalizados)
from django.views.decorators.csrf import requires_csrf_token
from django.template import loader
from django.http import HttpResponse

@requires_csrf_token
def csrf_failure(request, reason=""):
    try:
        t = loader.get_template('csrf_failure.html')
        return HttpResponse(
            t.render({'reason': reason}, request),
            status=403
        )
    except Exception:
        # Fallback si la plantilla no existe
        return HttpResponse(
            "<h1>Fallo de verificación CSRF</h1><p>{}</p>".format(reason),
            status=403
        )

# Luego, en settings.py, configura:
# CSRF_FAILURE_VIEW = 'blog.views.csrf_failure'
