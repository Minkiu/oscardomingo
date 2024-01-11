from datetime import datetime

from blog.models import Post, Tag
from django.shortcuts import get_list_or_404, get_object_or_404, render


def blog_index(request):
    posts = get_list_or_404(Post.objects.order_by('-created_on'))

    return render(
        request,
        "blog/index.html",
        {"posts": posts}
    )


def blog_post(request, post_uri):
    post = get_object_or_404(Post, uri=post_uri)

    return render(
        request,
        "blog/post.html",
        {"post": post}
    )


def blog_tag(request, tag_name):
    posts = get_list_or_404(Post.objects.filter(
        tags__name__contains=tag_name).order_by('-created_on'))

    return render(
        request,
        "blog/tag.html",
        {"posts": posts, "tag": tag_name}
    )


def blog_tags(request):
    tags = get_list_or_404(Tag.objects.order_by("name"))

    return render(
        request,
        "blog/tags.html",
        {"tags": tags}
    )
