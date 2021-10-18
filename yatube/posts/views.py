from django.contrib.auth import get_user_model
from django.core import paginator
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Group, Post


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10) 

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
        'post_list': post_list
    }
    return render(request, 'posts/index.html', context) 


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    post_list = Post.objects.filter(author=user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    post_counter = post_list.count
    page_obj = paginator.get_page(page_number)
    context = {
        'user_profile': user,
        'page_obj': page_obj,
        'post_counter': post_counter
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post,  pk=post_id)
    context = {   "post" : post,
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data['group']
            text = form.cleaned_data['text']
            return redirect('/profile/<username>/')
    context = {   
        'form':form
    }
    return render(request, 'posts/create.html', context)


def post_edit(request, post_id):
    post = get_object_or_404(Post,  pk=post_id)
 
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post.pk)
 
    if request.method != 'POST':
        post = get_object_or_404(Post,  pk=post_id)
        form = PostForm(post=post)
    else:
        form = PostForm(request.Post, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post.pk)
 
    context = {
        'form': form,
        'is_edit': True,
        'post': post,
    }
    return render(request, 'posts/create_post.html', context)
