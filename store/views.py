from django.shortcuts import get_object_or_404
from django.db.models import ProtectedError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ProductSerializer, CollectionSerializer
from .models import Product, Collection

# Create your views here.


class Products(APIView):
    def get(self, request):
        queryset = Product.objects.select_related(
            'collection').all().order_by('id')
        serializers = ProductSerializer(queryset, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializers = ProductSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)


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


class Collections(APIView):
    def get(self, request):
        queryset = Collection.objects.all().order_by('id')
        serializers = CollectionSerializer(queryset, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializers = CollectionSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)


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
