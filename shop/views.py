

from django.shortcuts import redirect, render, get_object_or_404, redirect

from .models import ContactUs, Genre, Product, Category, Feedback
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.views.generic.list import ListView

from django.contrib import  messages

from django.contrib.postgres.search import SearchVector
from .forms import SearchForm, ArticleForm, ProductForm, CommentForm, FeedbackForm, ContactUsForm

def user_is_admin(user):
    return user.is_superuser



class ContactListView(ListView):
    model = ContactUs
    template_name = "shop/contacted_users.html"
    paginate_by = 10

class FeedbackListView(ListView):
    model = Feedback
    template_name = "shop/feedback_list.html"
    paginate_by = 10
    

@login_required
def contact_us(request):
    if request.method=="POST":
            form = ContactUsForm(request.POST)
            if form.is_valid():
                form = form.save() 
                messages.success(request, 'Ваше сообщение отправлено успешно')
            return redirect('shop:contact_us')
    else:
        form = ContactUsForm()
    return render(request, 'account/contact_us.html', {'form':form})
    
    
@login_required
def feedback(request):
    if request.method=="POST":
            form = FeedbackForm(request.POST)
            if form.is_valid():
                form = form.save() 
                messages.success(request, 'Ваше сообщение отправлено успешно')
            return redirect('shop:send_feedback')
    else:
        form = FeedbackForm()
    return render(request, 'account/feedback.html', {'form':form})

@login_required
@user_passes_test(user_is_admin)
def add_product(request, type):   
    print("add ga kirvotti") 
    if type == "books":
        category = Category.objects.get(slug="books")
        if request.method=="POST":
            form = ProductForm(data = request.POST, files = request.FILES)
            if form.is_valid():
                product = form.save(commit=False) 
                print(request.POST)
                genre = Genre.objects.get(id = request.POST['genre'])
                product.category = category
                product.type = "book"
                product.content = request.POST['content']   
                product.save()                            
                product.genre.add(genre)
            return redirect('account:admin_dashboard')
        else:
            form = ProductForm()
        return render(request, 'shop/admin/add.html', {'form':form})
    elif type == "articles":
        category = Category.objects.get(slug="articles")
        if request.method == "POST":
            my_form = ArticleForm(data = request.POST, files =  request.FILES)
            print(request.POST)
            if my_form.is_valid():
                product = my_form.save(commit=False)
                product.category = category
                product.content = request.POST['content']
                product.type = "article"
                product.save()
            return redirect('account:admin_dashboard')
        else:
            my_form = ArticleForm()     
        return render(request,'shop/admin/add_article.html',{'myform':my_form})
      


@login_required 
def product_list(request, category_slug = None, genre_slug = None ):    
    if request.user.is_superuser:
        return redirect("account:admin_dashboard")       
    category = None
    genre = None
    categories = Category.objects.all()
    products = Product.objects.all()
    paginator = Paginator(products, 8)     
    if category_slug:
        category = get_object_or_404(Category, slug = category_slug)
        products = products.filter(category = category)
        paginator = Paginator(products, 8)
        
    if genre_slug:
        genre = get_object_or_404(Genre, slug = genre_slug)
        products = products.filter(genre = genre)
        paginator = Paginator(products, 8)
    genres = Genre.objects.all()
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'account/dashboard.html', {'category':category,
                                                      'categories':categories, 
                                                      'products':products,
                                                      'page_obj': page_obj,
                                                      'genres': genres,
                                                      'genr':genre
                                                      })


@login_required
def product_detail(request, id , slug):
    product = get_object_or_404(Product, id = id , slug = slug,available=True)
    
    comments = product.comments.filter(active=True)
    
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.save()
    else:
        comment_form = CommentForm()    
    
    return render( request, 'shop/product/detail.html', {'comment_form':comment_form,
                                                         'product':product, 
                                                         'comments': comments, 
                                                         'new_comment': new_comment})

def post_search(request):
    form = SearchForm() 
    query = None
    results = []
    if 'query' in request.GET:        
        query = request.GET.get('query')
        results = Product.objects.annotate(search=SearchVector('name', 'description'),).filter(search__icontains=query)
    return render(request,'shop/product/search.html',{'form': form,'query': query,'results': results})


def edit_product(request,product_id, product_slug, type):
    product = Product.objects.get(id = product_id, slug = product_slug)
    
    if type == "book":
        if request.method == 'POST':
            product_form = ProductForm(instance=product,data=request.POST, files=request.FILES)
            if product_form.is_valid():
                product_form.save()
            return redirect("account:dashboard")
        else:
            product_form = ProductForm(instance=product) 
    elif type == "article":
        if request.method == 'POST':
            product_form = ArticleForm(instance=product,data=request.POST, files=request.FILES)
            if product_form.is_valid():
                product_form.save()
            return redirect("account:dashboard")
        else:
            product_form = ArticleForm(instance=product)
    return render(request,'shop/product/edit.html',{'product_form': product_form, 'product': product})
    

# end of the file


    