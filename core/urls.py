from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

admin.site.site_header = 'Shopino Store'
admin.site.index_title = 'Shopino Admin Panel'