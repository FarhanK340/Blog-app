from django.urls import path
from .views import BlogView

app_name = 'blog'
urlpatterns = [
    path('', BlogView.as_view() , name = 'blog_list'),
    path('create/', BlogView.as_view() , name='blog_create'),
    path('<int:id>/<str:title>/', BlogView.as_view() , name='blog_detail'),
]
    