# from django.urls import path,include
# from . import views
# #from django.views.generic import TemplateView
# urlpatterns = [
#     path('',views.index,name="blog"),
#
#     #path("blogPost/<int:id>", views.blogpost, name="blogHome")
#      #path("blogPost/", TemplateView.as_view(template_name='index.html'))
#     # it is templateView is use when we need to direct go to the html page without any logic or calculation
# ]

from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.index, name="blog-home"),
    path("blogPost/<int:id>", views.blogPost, name="blog-Post"),
]