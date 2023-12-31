from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .forms import CommentForm, ProfileForm
from .models import Post, Profile, Short, Comment, SavedPosts, Notification
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib import messages
from django.db.models import Q


def homepage(request):
    context = {}
    posts_list = Post.objects.all()
    context['posts'] = posts_list
    shorts_list = Short.objects.all()
    context["shorts"] = shorts_list
    return render(request, 'home.html', context)


def post_detail(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    context['post'] = post_object
    comment_form = forms.CommentForm()
    context['comment_form'] = comment_form
    comments_list = Comment.objects.filter(post=post_object)
    context['comments'] = comments_list
    if request.method == 'GET':
        return render(request, 'post_info.html', context)
    elif request.method == 'POST':
        if 'like' in request.POST:
            post_object.likes += 1
            post_object.save()

            Notification.objects.create(user=post_object.user,
                                        text=f"{request.user.profile.nickname} liked your post")
            return redirect(post_detail, id=id)
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.created_by = request.user
                new_comment.post = post_object
                new_comment.save()

                Notification.objects.create(user=post_object.user, text=f"{request.user.profile.nickname} commented your post")
                return redirect(post_detail, id=id)


def profile_detail(request, id):
    context = {}
    profile = Profile.objects.get(id=id)
    context['profile'] = profile

    return render(request, 'profile_detail.html', context)


def shorts(request):
    context = {'shorts_list': Short.objects.all()}
    return render(request, "shorts.html", context)


def short_info(request, id):
    short = Short.objects.get(id=id)
    short.views_qty += 1
    short.viewed_users.add(request.user)
    short.save()
    context = {"short": short}
    return render(request, "shorts_info.html", context)


def update_short(request, id):
    short = Short.objects.get(id=id)
    if request.method == "POST":
        new_description = request.POST["description"]
        short.description = new_description
        short.save()
        return redirect(short_info, id=short.id)

    context = {'short': short}
    return render(request, 'update_short.html', context)


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
        new_post = Post()
        new_post.name = data['post_name']
        new_post.description = data['description']
        new_post.user = request.user
        new_post.photo = request.FILES['photo']
        new_post.save()
        return redirect(homepage)


def add_post_form(request):
    if request.method == "POST":
        post_form = forms.PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_object = post_form.save(commit=False)
            post_object.user = request.user
            post_object.save()
            return redirect(post_detail, id=post_object.id)
        else:
            messages.warning(request, f"Form doesn't valid: {post_form.errors}")

    post_form = forms.PostForm()
    context = {"post_form": post_form}
    return render(request, 'create_post_django_form.html', context)


def update_post(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    if request.user != post_object.user:
        return redirect(homepage)
    if request.method == "POST":
        post_form = forms.PostForm(data=request.POST, files=request.FILES, instance=post_object)
        if post_form.is_valid():
            post_form.save()
            return redirect(post_detail, id=post_object.id)
        else:
            messages.warning(request, "Form doesn't valid")
            context["post_form"] = post_form
            return render(request, 'update_post.html', context)
    post_form = forms.PostForm(instance=post_object)
    context["post_form"] = post_form
    return render(request, 'update_post.html', context)


def delete_post(request, id):
    post = Post.objects.get(id=id)

    if request.user != post.user:
        return redirect(homepage)
    post.delete()
    return redirect(user_posts, user_id=request.user.id)


@login_required(login_url='/users/sign_in/')
def add_short(request):
    if request.method == 'GET':
        return render(request, 'short_form.html')
    elif request.method == 'POST':
        new_short_object = Short(user=request.user, video=request.FILES['video_file'],)
        new_short_object.save()
        return redirect('shorts-info', id=new_short_object.id)


def add_saved(request):
    if request.method == "POST":
        post_id = request.POST['post_id']
        post_object = Post.objects.get(id=post_id)
        saved_post, _ = SavedPosts.objects.get_or_create(user=request.user)
        saved_post.post.add(post_object)
        saved_post.save()
        return redirect('/saved_posts/')


# def search(request):
#     return render(request, 'search.html')


def search_result(request):
    key_word = request.GET["key_word"]
    posts = Post.objects.filter(Q(name__icontains=key_word) | Q(description__icontains=key_word))
    context = {"posts": posts}
    return render(request, 'home.html', context)


def subscribe(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if request.user in profile.subscribers.all():
        profile.subscribers.remove(request.user)
        profile.save()
        messages.success(request, 'You have successfully unsubscribed')
        return redirect(f'/posts/profile/{profile.id}/')
    else:
        profile.subscribers.add(request.user)
        profile.save()
        messages.success(request, "You have successfully subscribed")
        new_notification = Notification(user=profile.user, text=f"{request.user.username} subscribed you")
        new_notification.save()
        return redirect(f'/posts/profile/{profile.id}/')


def notifications(request):
    notifications_list = Notification.objects.filter(user=request.user)
    for notification in notifications_list:
        notification.is_showed = True
    Notification.objects.bulk_update(notifications_list, ['is_showed'])
    context = {"notifications": notifications_list}
    return render(request=request, template_name='notifications.html', context=context)


def add_profile(request):
    profile_form = ProfileForm()
    context = {'profile_form': profile_form}

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_object = profile_form.save(commit=False)
            profile_object.user = request.user
            profile_object.save()
            return redirect(profile_detail, id=profile_object.id)
        else:
            return HttpResponse("Not valid")

    return render(request, 'add_profile.html', context)


def comment_delete(request, id):
    comment = Comment.objects.get(id=id)

    if request.user != comment.created_by:
        messages.warning(request, "You haven't got permission to do it")
        return redirect(post_detail, id=comment.post.id)

    comment.delete()
    return redirect(post_detail, id=comment.post.id)


class SubscriptionsView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        user_object = User.objects.get(id=kwargs['user_id'])
        profiles_list = user_object.followed_profile.all()
        context = {"profiles_list": profiles_list}
        return render(request, 'subscriptions.html', context)