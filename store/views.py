from django.shortcuts import get_object_or_404
from django.db.models import ProtectedError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from .serializers import ProductSerializer, CollectionSerializer
from .models import Product, Collection

# Create your views here.


class Products(ListCreateAPIView):
    queryset = Product.objects.select_related(
        'collection').all().order_by('id')
    serializer_class = ProductSerializer

class ProductDetail(APIView):
    def get(self, request, pk):
        queryset = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        queryset = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def delete(self, request, pk):
        queryset = get_object_or_404(Product, pk=pk)
        try:
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({'message': 'Product cannot be deleted because it is associated with an OrderItem .'}, status=status.HTTP_404_NOT_FOUND)


class Collections(ListCreateAPIView):
    queryset = Collection.objects.all().order_by('id')
    serializer_class = CollectionSerializer


class CollectionDetail(APIView):
    def get(self, request, pk):
        queryset = get_object_or_404(Collection, pk=pk)
        serializer = CollectionSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        queryset = get_object_or_404(Collection, pk=pk)
        serializer = CollectionSerializer(queryset, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        queryset = get_object_or_404(Collection, pk=pk)
        try:
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response({'message': 'Collection cannot be deleted because it is associated with an product .'}, status=status.HTTP_404_NOT_FOUND)
