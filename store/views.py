from django.shortcuts import get_object_or_404
from django.db.models import ProtectedError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer, CollectionSerializer
from .models import Product, Collection

# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer

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
