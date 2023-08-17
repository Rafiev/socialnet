from django.shortcuts import render, HttpResponse, redirect
from .models import Post, Profile, Short
from django.contrib.auth.models import User
from . import forms


def homepage(request):
    context = {'name': 'Emirlan'}
    posts_list = Post.objects.all()
    context['posts'] = posts_list
    return render(request, 'home.html', context)


def post_detail(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    context['post'] = post_object
    comment_form = forms.CommentForm()
    context['comment_form'] = comment_form
    if request.method == 'GET':
        return render(request, 'post_info.html', context)
    elif request.method == 'POST':
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.created_by = request.user
            new_comment.post = post_object
            new_comment.save()
            return redirect(post_detail, id=id)



def profile_detail(request, id):
    context = {'profile': Profile.objects.get(id=id)}
    return render(request, 'profile_detail.html', context)


def shorts(request):
    context = {'shorts_list': Short.objects.all()}
    return render(request, "shorts.html", context)


def short_info(request, id):
    context = {"short": Short.objects.get(id=id)}
    return render(request, "short_info.html", context)


def saved_posts(request):
    posts = Post.objects.filter(saved_posts__user=request.user)
    context = {'posts': posts}
    return render(request, 'saved_posts.html', context)


def user_posts(request, user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(user=user)
    context = {'user': user, 'posts': posts}
    return render(request, 'user_posts.html', context)


def create_post(request):
    if request.method == 'GET':
        return render(request, 'create_post_form.html')
    elif request.method == 'POST':
        data = request.POST
        print(data)
        new_post = Post()
        new_post.name = data['post_name']
        new_post.description = data['description']
        new_post.user = request.user
        new_post.photo = request.FILES['photo']
        new_post.save()
        return render(request, 'home.html')