from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Comment
from .forms import PostForm, CommentForm

@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            return redirect('detalle_publicacion', pk=publicacion.pk)
    else:
        form = PostForm()
    return render(request, 'blog/crear_publicacion.html', {'form': form})

@login_required
def editar_publicacion(request, pk):
    publicacion = get_object_or_404(Post, pk=pk)
    if publicacion.autor != request.user:
        return HttpResponseForbidden("No tienes permiso para editar esta publicación.")
    if request.method == 'POST':
        form = PostForm(request.POST, instance=publicacion)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            return redirect('detalle_publicacion', pk=publicacion.pk)
    else:
        form = PostForm(instance=publicacion)
    return render(request, 'blog/editar_publicacion.html', {'form': form})

@login_required
def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(Post, pk=pk)
    if publicacion.autor == request.user:
        publicacion.delete()
    return redirect('lista_publicaciones')

@login_required
def agregar_comentario(request, pk):
    publicacion = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.publicacion = publicacion
            comentario.save()
            return redirect('detalle_publicacion', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/agregar_comentario.html', {'form': form})