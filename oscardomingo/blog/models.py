from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=300)
    uri = models.CharField(max_length=300)
    tags = models.ManyToManyField("Tag", related_name="posts")

    def __str__(self):
        return self.title
