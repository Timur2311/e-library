
from dataclasses import field
from django import forms
from django.forms import ModelForm
from .models import Genre, Product, Comment, Feedback, ContactUs

from django.forms import Select

class ProductForm(ModelForm):  
    genre =  forms.ChoiceField(choices=[(genre.id, genre.name) for genre in Genre.objects.all()])  
    class Meta:        
        model = Product
        fields = ['name','image','author','genre','file','content']
        widgets = { 'genre': Select(attrs={'class': 'select'})}      
        
class SearchForm(forms.Form):
    query = forms.CharField()
    
class ArticleForm(ModelForm):
    # content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Product
        fields = ['name', 'image', 'author','content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')        

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields=("__all__")
        
class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields=("__all__")
        





# class ProductForm(forms.Form):
    
#     users = User.objects.all()
#     genres = Genre.objects.all()
#     USERS_CHOICES = ('','')
#     GENRES_CHOICES = ('','')
#     for user in users:
#         USERS_CHOICES+=("{{user.name}}","{{user.name}}")   
#     for genre in genres:
#         GENRES_CHOICES+=("{{genre.name}}","{{genre.name}}") 
#     name = forms.CharField(label='Название', max_length=100)
#     image = forms.ImageField()
#     author = forms.CharField(choices=USERS_CHOICES)
#     genre = forms.CharField(choices=GENRES_CHOICES)
#     file = forms.FileField()
#     content = forms.CharField(widget=CKEditorWidget())
    

