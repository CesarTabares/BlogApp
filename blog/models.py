from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    author= models.ForeignKey('auth.User', on_delete=models.CASCADE) # si el autor John , crea 10 post y elimino este autor, todos los post se eliminaran
    title= models.CharField(max_length=200)
    text=models.TextField()
    created_date= models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True,null=True)

    def published(self):
        self.published_date=timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post=models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments') # Si elimino el blog post, todos los comentarios relacionados con el , se eliminan, ya que es una foreing key
    author=models.CharField(max_length=200)
    text= models.TextField()
    created_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
