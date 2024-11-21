from django.contrib.auth import get_user_model
from rest_framework import serializers

from cart.models import ProductInCart
from categories.models import Category, Subcategory
from products.models import Product, ProductImage


class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = ('name', 'slug', 'id', 'image')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'id', 'image', 'subcategories')


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('image',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='subcategory.category.name')
    subcategory = serializers.CharField(source='subcategory.name')
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ('name', 'slug', 'category', 'subcategory', 'price', 'images')


class ProductInCartSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=True,
    )

    class Meta:
        model = ProductInCart
        fields = ('product', 'amount')


class UserCartSerializer(serializers.ModelSerializer):
    products_in_cart = ProductInCartSerializer(many=True, read_only=True)
    cost = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'products_in_cart', 'cost')

    def get_cost(self, user):
        return sum(
            (p.amount * p.product.price for p in user.products_in_cart.all())
        )
