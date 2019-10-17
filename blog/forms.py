from django import forms
from .models import Post


# se genera este archivo "forms.py" para indicarle a Django que genere un formulario , con ciertos campos que ya fueron creados en models.py

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title','text')
