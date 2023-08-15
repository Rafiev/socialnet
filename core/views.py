from django.shortcuts import render, HttpResponse
from .models import Post, Profile, Short
from django.contrib.auth.models import User


def homepage(request):
    context = {'name': 'Emirlan'}
    posts_list = Post.objects.all()
    context['posts'] = posts_list
    return render(request, 'home.html', context)


def post_detail(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    context['post'] = post_object
    return render(request, 'post_info.html', context)


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