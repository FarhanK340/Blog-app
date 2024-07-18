from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Blog
from .forms import BlogForm, SignUpForm


def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, "blog/blog_list.html", {"blogs": blogs})


@login_required
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect("blog:blog_list")
    else:
        form = BlogForm()
    return render(request, 'blog/blog_create.html', {"form": form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user.set_password(raw_password)
            user.save()
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('blog:blog_list')
    else:
        form = SignUpForm()
    return render(request, 'blog/registration/signup.html', {'form': form})
