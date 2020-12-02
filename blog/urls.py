from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.index, name="blog-home"),
    path("blogPost/<int:id>", views.blogPost, name="blog-Post"),
]