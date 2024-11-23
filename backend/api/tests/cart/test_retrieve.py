from rest_framework import status

from cart.models import ProductInCart
from .base import CartEndpoinTestCase


class TestCartRetriveEndpoint(CartEndpoinTestCase):

    def test_anon_request_fails(self):
        self.do_request_and_check_response(
            self.client, (), status.HTTP_401_UNAUTHORIZED
        )

    def test_auth_request_ok_if_cart_empty(self):
        exp_response_data = dict(
            username=self.fixture_user.username,
            products_in_cart=[],
            cost=0,
        )
        self.do_auth_request_and_check_response(
            exp_response_data, status.HTTP_200_OK
        )

    def test_auth_request_ok_if_cart_not_empty(self):
        self.maxDiff = None
        amount = 2
        ProductInCart.objects.bulk_create(
            ProductInCart(
                user=self.fixture_user,
                product=self.fixture_products[i],
                amount=amount
            )
            for i in range(len(self.fixture_products))
        )
        exp_response_data = dict(
            username=self.fixture_user.username,
            products_in_cart=[
                dict(product=product.name, amount=amount)
                for product in self.fixture_products
            ],
            cost=(
                amount
                * sum(product.price for product in self.fixture_products)
            ),
        )
        self.do_auth_request_and_check_response(
            exp_response_data, status.HTTP_200_OK
        )

    def do_auth_request_and_check_response(
        self, exp_response_data, exp_status
    ):
        client = self.create_auth_client(self.fixture_user)
        return self.do_request_and_check_response(
            client, exp_response_data, exp_status
        )

    def do_request_and_check_response(
        self, client, exp_response_data, exp_status
    ):
        return super().do_request_and_check_response(
            client, 'get', '/api/cart/', None, exp_response_data, exp_status
        )
