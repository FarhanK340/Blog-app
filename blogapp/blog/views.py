from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 
from django.contrib.auth import login, authenticate
from django.views.generic import View
from .models import Blog
from .forms import BlogForm, SignUpForm

class BlogView(View):
    def get(self, request, *args, **kwargs):
        if 'id' in kwargs and 'title' in kwargs:
            return self.blog_detail(request, kwargs['id'])
        else:
            return self.blog_list(request)


    def post(self, request, *args, **kwargs):
        if request.path == '/accounts/signup/':
            return self.signup(request)
        return self.blog_create(request)

    def blog_list(self, request):
        blogs = Blog.objects.all()
        return render(request, "blog/blog_list.html", {"blogs": blogs})


    @method_decorator(login_required)
    def blog_create(self, request):
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


    def signup(self, request):
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
    

    def blog_detail(self, request, id):
        blog = Blog.objects.get(id=id)
        return render(request, 'blog/blog_detail.html', {'blog': blog})
