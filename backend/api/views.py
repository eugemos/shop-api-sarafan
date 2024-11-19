from rest_framework import generics

from categories.models import Category
from products.models import Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().prefetch_related('subcategories')
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().prefetch_related(
        'images'
    ).order_by(
        'subcategory__category', 'subcategory'
    )

    serializer_class = ProductSerializer
