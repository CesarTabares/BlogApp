from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm, UserForm
# Create your views here.


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    stuff_for_frontent = {'posts':posts}
    return render(request, 'blog/post_list.html', stuff_for_frontent)

def post_detail(request,pk):
    post = get_object_or_404 (Post,pk=pk)
    stuff_for_frontent={'post':post}
    return render(request, 'blog/post_detail.html',stuff_for_frontent)

@login_required
def post_new(request):
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False) #el form es como guardar un registro nuevo, es decir convierte este registro en un objeto nuevo
            print(post)
            post.author= request.user
            #post.published_date=timezone.now()
            post.save()
            print ('cesar')
            return redirect ('post_detail', pk=post.pk)
    else:
        #print(request.POST)
        form=PostForm()
        stuff_for_frontent={'form':form}
        return render(request, 'blog/post_edit.html', stuff_for_frontent)
@login_required
def post_edit (request, pk):
    post= get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=PostForm(request.POST, instance=post) # instance es necesario aca, pq si no se pone el toma cuando se le de guardar al post editado, crea uno nuevo
        #Instance , esta asignando un form ya existente llamad post, para que traiga los datos ya guardados, y no
        #un formulario nuevo
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            #post.published_date=timezone.now()
            post.published_date=None
            post.save()
            return redirect('post_detail' , pk=post.pk)
    else:
        form=PostForm(instance=post)
        stuff_for_frontent={'form':form , 'post':post}
        return render(request, 'blog/post_edit.html', stuff_for_frontent)

@login_required
def post_draft_list(request):
    posts=Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    stuff_for_frontent={'posts': posts}
    return render(request, 'blog/post_draft_list.html' , stuff_for_frontent)

@login_required
def post_publish(reques,pk):
    post=get_object_or_404(Post,pk=pk)
    post.published()
    return redirect ('post_detail', pk=pk)

@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False) # we don't want to commit this to the database , WTF ????
            comment.author=request.user
            comment.post=post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form=CommentForm()
        return render(request, 'blog/add_comment_to_post.html',{'form':form})
@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.delete()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@staff_member_required
def post_delete(request,pk):
    
    post=get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('/') #se hizo hardcode, pq si se pone redirect ('post_list') , esta url debe recibir una pk, pero como ya eliminamos el posts
    #no es posible obtener la pk


def signup(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            new_user=User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('/')
    else:
        form=UserForm()
    return render(request, 'registration/signup.html', {'form': form})
