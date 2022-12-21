from django.shortcuts import get_object_or_404
from django.db.models import ProtectedError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from .models import Product, Collection, Review
from .filter import ProductFilter

# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def destroy(self, request, pk):
        queryset = get_object_or_404(Product, pk=pk)
        try:
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({'message': 'Product cannot be deleted because it is associated with an OrderItem .'}, status=status.HTTP_404_NOT_FOUND)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all().order_by('id')
    serializer_class = CollectionSerializer

    def destroy(self, request, pk):
        queryset = get_object_or_404(Collection, pk=pk)
        try:
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({'message': 'Collection cannot be deleted because it is associated with an product .'}, status=status.HTTP_404_NOT_FOUND)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk_pk']).order_by('id')

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk_pk']}
