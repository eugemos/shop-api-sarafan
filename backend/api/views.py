from django import http
# from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response

from cart.models import ProductInCart
from categories.models import Category
from products.models import Product
from .serializers import (
    CategorySerializer, ProductSerializer,
    ProductInCartSerializer,
    UserCartSerializer
)


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


class ProductInCartView(
    mixins.CreateModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, generics.GenericAPIView
):
    serializer_class = ProductInCartSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'product__slug'
    lookup_url_kwarg = 'product'

    def get_queryset(self):
        return ProductInCart.objects.filter(user=self.request.user)

    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except http.Http404:
            return self.create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            return self.add_amount(request, *args, **kwargs)
        except http.Http404:
            return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            product=get_object_or_404(Product, slug=self.kwargs['product']),
            user=self.request.user
        )

    def add_amount(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['amount'] += instance.amount
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    # def create(self, )


class CartView(generics.RetrieveDestroyAPIView):
    # queryset = get_user_model().objects.all().prefetch_related(
    #     'products_in_cart'
    # )
    serializer_class = UserCartSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
