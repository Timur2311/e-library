
from django.urls import path
from . import views
from .views import FeedbackListView, ContactListView

app_name = 'shop'

urlpatterns = [
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('genre/<slug:genre_slug>/', views.product_list, name='product_list_by_genre'),
    path('addProduct/<str:type>', views.add_product, name = 'add_product'),
    path('search/', views.post_search, name='post_search'), 
    path('feedback/',views.feedback, name="send_feedback"),
    path('contactus/',views.contact_us , name="contact_us"),
    path('contacted_users/', ContactListView.as_view(), name="contacted_users_list"),
    path('sended_feedbacks/', FeedbackListView.as_view(), name="feedback_list"),            
    
    
    path('', views.product_list, name='product_list'), 
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('edit/<int:product_id>/<slug:product_slug>/<str:type>', views.edit_product, name = "edit_product")
    
    
    
]
