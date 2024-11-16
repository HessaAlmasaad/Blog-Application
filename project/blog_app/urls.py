from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('blogs', views.allblogs),
    path('blogs/create', views.create_blog),
    path('blogs/<cat>', views.allcat),
    path('blogs/view/<id>', views.blog_dis),
    path('add_likes/<id>',views.add_likes),
    path('blogs/<id>/delete', views.del_blog),
]
