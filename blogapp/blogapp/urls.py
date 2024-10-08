
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from blog import views


urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='blog/registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(
        next_page='login'), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
