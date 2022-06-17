from django.contrib import admin

from .models import Product, Genre,Category, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','available','created','updated']
    list_filter = ['available','created','updated']
    list_editable = [ 'available']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product','name', 'email', 'body']
    