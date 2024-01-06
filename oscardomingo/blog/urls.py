from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_index, name="index"),
    path("post", views.blog_post, name="post"),
    path("tag/<str:tag_name>", views.blog_tag, name="tag"),
    path("tags", views.blog_tags, name="tags")
]
