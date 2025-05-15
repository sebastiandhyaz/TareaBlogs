from django.shortcuts import render, redirect, get_object_or_404
from .models import Publicacion, Comentario
from .forms import PublicacionForm, ComentarioForm

# Create your views here.
def lista_publicaciones(request):
    publicaciones = Publicacion.objects.all()  # select * from publicacion
    return render(request,'blog/lista_publicaciones.html', {'publicaciones':publicaciones})

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
