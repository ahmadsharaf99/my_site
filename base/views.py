from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .models import Post
from .filters import PostFilter
from .forms import PostForm


def home(request):
    blog_posts = Post.objects.filter(active=True, featured=True)[:3]
    return render(request, "base/index.html", context={'posts': blog_posts})


def posts(request):
    blog_posts = Post.objects.filter(active=True)
    my_filter = PostFilter(request.GET, queryset=blog_posts)
    blog_posts = my_filter.qs

    page = request.GET.get('page')
    paginator = Paginator(blog_posts, 3)

    try:
        blog_posts = paginator.page(page)
    except PageNotAnInteger:
        blog_posts = paginator.page(1)
    except EmptyPage:
        blog_posts = paginator.page(paginator.num_pages)

    context = {'posts': blog_posts, 'my_filter': my_filter}
    return render(request, "base/posts.html", context=context)


def post(request, slug):
    blog_post = Post.objects.get(slug=slug)
    return render(request, "base/post.html", context={'post': blog_post})


def profile(request):
    return render(request, "base/profile.html")


# CRUD views
@login_required(login_url='home')
def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('posts')

    return render(request, 'base/post_form.html', context={'form': form})


@login_required(login_url='home')
def update_post(request, slug):
    blog_post = Post.objects.get(slug=slug)
    form = PostForm(instance=blog_post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=blog_post)
        if form.is_valid():
            form.save()
        return redirect('posts')

    return render(request, 'base/post_form.html', context={'form': form})


@login_required(login_url='home')
def delete_post(request, slug):
    blog_post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        blog_post.active = False
        blog_post.save()
        return redirect('posts')

    return render(request, 'base/delete.html', {'item': blog_post})


def send_email(request):
    if request.method == 'POST':
        template = render_to_string('base/email_template.html', {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })
        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['ahmadsharafudeen98@gmail.com'],
        )
        email.fail_silently = False
        email.send()
    return render(request, 'base/email_sent.html')
