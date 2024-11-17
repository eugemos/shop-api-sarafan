from django.db import models


class AbstractCategory(models.Model):
    IMAGES_UPLOAD_PATH = 'categories/'

    name = models.CharField('наименование', max_length=150)
    slug = models.SlugField('обозначение', unique=True)
    image = models.ImageField(
        'изображение', upload_to=IMAGES_UPLOAD_PATH, blank=True, null=True
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(AbstractCategory):

    class Meta(AbstractCategory.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Subcategory(AbstractCategory):
    category = models.ForeignKey(
        Category,
        verbose_name='категория',
        on_delete=models.CASCADE,
        related_name='subcategories',
    )

    class Meta(AbstractCategory.Meta):
        verbose_name = 'подкатегория'
        verbose_name_plural = 'подкатегории'
