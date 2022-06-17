
from django.shortcuts import redirect, render


from django.shortcuts import render


from .forms import UserRegistrationForm


from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User



from shop.models import Category, Product
from django.core.paginator import Paginator

from django.contrib.auth.decorators import user_passes_test
from shop.views import user_is_admin

@login_required
def dashboard(request):
    products = Product.objects.all()
    categories =  Category.objects.all()
    if request.user.is_superuser:
        return redirect('account:admin_dashboard')
    paginator = Paginator(products, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request,'account/dashboard.html',{'section': 'dashboard','page_obj': page_obj,'products':products,'categories': categories})


@login_required
@user_passes_test(user_is_admin)
def admin_dashboard(request):
    products = Product.objects.all()
    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == "GET":
        if 'delete_book' in request.GET:
            product_id = request.GET.get('delete_book')
            product = Product.objects.get(id = product_id)
            product.delete()
            return redirect("account:admin_dashboard")
    return render(request,'account/user/admin/admin_dashboard.html',{'section': 'dashboard','page_obj': page_obj,'products':products})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            
            return render(request,'account/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})





    


    

