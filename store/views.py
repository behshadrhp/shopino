from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, CollectionSerializer
from .models import Product, Collection

# Create your views here.


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related(
            'collection').all().order_by('id')
        serializers = ProductSerializer(queryset, many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        serializers = ProductSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    queryset = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(queryset)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        if queryset.orderitems.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.all().order_by('id')
        serializers = CollectionSerializer(queryset, many=True)
        return Response(serializers.data)
    if request.method == 'POST':
        serializers = CollectionSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)
