from django.contrib.auth import get_user_model

from categories.models import Category, Subcategory
from products.models import Product
from ..base import EndpointTestCase

User = get_user_model()


class CartEndpoinTestCase(EndpointTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        category = Category.objects.create(
            name='Category-1', slug='category-1'
        )
        subcategory = Subcategory.objects.create(
            name='Subcategory-1', slug='subcategory-1', category=category
        )
        cls.fixture_products = Product.objects.bulk_create(
            Product(
                name=f'Product-{i}',
                slug=f'product-{i}',
                price=i,
                subcategory=subcategory,
            )
            for i in range(1, 4)
        )
        cls.fixture_user = User.objects.create_user(
            username='user-1', email='user-1@example.com'
        )
