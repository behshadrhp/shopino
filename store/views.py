from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product

# Create your views here.

@api_view()
def product_list(request):
    queryset = Product.objects.select_related('collection').all().order_by('id')
    serializers = ProductSerializer(queryset, many=True)
    return Response(serializers.data)


@api_view()
def product_detail(request, pk):
    queryset = Product.objects.get(pk=pk)
    serializer = ProductSerializer(queryset)
    return Response(serializer.data)