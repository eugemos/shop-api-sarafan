from django.contrib import admin

from .models import Product, ProductImage


class ImageInline(admin.TabularInline):
    model = ProductImage
    max_num = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройки отображения модели Product в административной панели."""
    list_display = ('name', 'price', 'subcategory', 'category')
    list_filter = ('subcategory__category', 'subcategory')
    readonly_fields = ('category',)
    inlines = (ImageInline,)
