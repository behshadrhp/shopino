from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.Products.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('collections/', views.Collections.as_view()),
    path('collections/<int:pk>', views.CollectionDetail.as_view()),
]
