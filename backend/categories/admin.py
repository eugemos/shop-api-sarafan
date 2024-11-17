from django.contrib import admin

from .models import Category, Subcategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройки отображения модели Category в административной панели."""
    list_display = ('name', )


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """Настройки отображения модели Subcategory в административной панели."""
    list_display = ('name', 'category')
    list_filter = ('category', )
