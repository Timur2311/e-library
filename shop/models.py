from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils.text import slugify

from ckeditor_uploader.fields import RichTextUploadingField


from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True)    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name    
    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", args=[self.slug])
  

    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='category_products', on_delete=models.CASCADE, verbose_name="Категория")
    genre = models.ManyToManyField('Genre', verbose_name="Выберите жанр", related_name='genres')
    type = models.CharField(max_length=200,blank=True, null=True)
    author = models.ForeignKey('auth.User',related_name='user_products',on_delete=models.CASCADE, verbose_name="Автор", blank=True,null=True)
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to = 'books/%Y/%m/%d', blank=True, verbose_name="Обложка")
    file = models.FileField(upload_to='books/pdf/%Y/%m/%d', blank = True, verbose_name="Файл Книги")
    description = models.TextField(blank=True, verbose_name="Описание")    
    content = RichTextUploadingField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-id',)
        index_together = (('id','slug'),)
        
        def __str__(self):
            return self.name
    
    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])
    
    def save(self,*args,**kwargs):
        i = 1
        text = slugify(self.name)        
        while Product.objects.filter(slug = text).exists() :
            i+=1            
            text = slugify(f"{text}+{i}")                           
        self.slug=slugify(text)        
        super(Product,self).save(*args,**kwargs)
  
  
class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80, verbose_name='Имя')
    email = models.EmailField( verbose_name='Почта')
    body = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return f'Comment by {self.name} on {self.product}'
        
    

class Genre(models.Model):
    name = models.CharField(max_length=200, db_index=True,verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True)     
    category = models.ForeignKey(Category, related_name='genres', on_delete=models.CASCADE)
    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    
    def __str__(self):
        return self.name 
       
    
    
    def save(self,*args,**kwargs):
        i = 1
        text = slugify(self.name)        
        while Genre.objects.filter(slug = text).exists() :
            i+=1            
            text = slugify(f"{text}+{i}")                           
        self.slug=slugify(text)        
        super(Genre,self).save(*args,**kwargs)
        
    def get_absolute_url(self):
        return reverse("shop:product_list_by_genre", args=[self.slug])
    
    
class Feedback(models.Model):
    text = models.TextField(max_length = 1000, null=True,  blank=True, verbose_name="Сообщение")

class ContactUs(models.Model):
    name = models.CharField(max_length=200,verbose_name="Введите имю", blank=True)
    callback = models.CharField(max_length=200, verbose_name="Контакт для обратной связи")
    client_message = models.TextField(max_length=1000, verbose_name="Сообщение")