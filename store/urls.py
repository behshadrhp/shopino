from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

products_router = NestedDefaultRouter(router, 'products', lookup='product_pk')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-reviews')

urlpatterns = router.urls + products_router.urls