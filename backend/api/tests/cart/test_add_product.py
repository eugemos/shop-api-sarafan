from rest_framework import status

from cart.models import ProductInCart
from .base import CartEndpoinTestCase


class TestCartAddProductEndpoint(CartEndpoinTestCase):

    def test_anon_request_fails(self):
        product_slug = self.fixture_products[0].slug
        request_data = dict(amount=2)
        self.do_request_and_check_response(
            self.client, product_slug, request_data, (),
            status.HTTP_401_UNAUTHORIZED
        )

    def test_auth_request_with_nonexistent_product_fails(self):
        product_slug = 'nonexistent_product'
        request_data = dict(amount=2)
        self.do_auth_request_and_check_response(
            product_slug, request_data, (), status.HTTP_404_NOT_FOUND
        )

    def test_auth_request_with_incorrect_amount_fails(self):
        product_slug = self.fixture_products[0].slug
        request_data = dict(amount=0)
        self.do_auth_request_and_check_response(
            product_slug, request_data, (), status.HTTP_400_BAD_REQUEST
        )

    def test_auth_request_without_amount_fails(self):
        product_slug = self.fixture_products[0].slug
        request_data = dict()
        self.do_auth_request_and_check_response(
            product_slug, request_data, (), status.HTTP_400_BAD_REQUEST
        )

    def test_auth_request_to_create_ok(self):
        amount = 1
        product_slug = self.fixture_products[0].slug
        request_data = dict(amount=amount)
        exp_response_data = dict(
            product=self.fixture_products[0].name,
            amount=amount
        )
        self.do_auth_request_and_check_response(
            product_slug, request_data, exp_response_data,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            ProductInCart.objects.filter(
                product=self.fixture_products[0],
                user=self.fixture_user,
                amount=amount,
            ).count(),
            1
        )

    def test_auth_request_to_add_ok(self):
        amount_before = 1
        ProductInCart.objects.create(
            product=self.fixture_products[0],
            user=self.fixture_user,
            amount=amount_before
        )
        amount_to_add = 1
        product_slug = self.fixture_products[0].slug
        request_data = dict(amount=amount_to_add)
        exp_amount_after = amount_before + amount_to_add
        exp_response_data = dict(
            product=self.fixture_products[0].name,
            amount=exp_amount_after
        )
        self.do_auth_request_and_check_response(
            product_slug, request_data, exp_response_data,
            status.HTTP_200_OK
        )
        self.assertEqual(
            ProductInCart.objects.filter(
                product=self.fixture_products[0],
                user=self.fixture_user,
                amount=exp_amount_after,
            ).count(),
            1
        )

    def do_auth_request_and_check_response(
        self, product_slug, request_data, exp_response_data, exp_status
    ):
        client = self.create_auth_client(self.fixture_user)
        return self.do_request_and_check_response(
            client, product_slug, request_data, exp_response_data, exp_status
        )

    def do_request_and_check_response(
        self, client, product_slug, request_data,
        exp_response_data, exp_status
    ):
        return super().do_request_and_check_response(
            client, 'post', f'/api/cart/{product_slug}/', request_data,
            exp_response_data, exp_status
        )
