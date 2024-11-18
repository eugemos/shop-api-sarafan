from rest_framework import serializers

from categories.models import Category, Subcategory


class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = ('name', 'slug', 'id', 'image')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'id', 'image', 'subcategories')
