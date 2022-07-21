from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('shop.urls', namespace='shop')),
    path('admin/', admin.site.urls),
    path('account/',include('account.urls')),    
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),   
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
