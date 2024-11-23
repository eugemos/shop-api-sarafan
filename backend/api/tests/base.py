from rest_framework.test import APIClient, APITestCase


class EndpointTestCase(APITestCase):

    def create_auth_client(self, user):
        auth_client = APIClient()
        auth_client.force_authenticate(user=user)
        return auth_client

    def do_request_and_check_response(
        self, client, method, url, request_data,
        exp_response_data, exp_status, **kwargs
    ):
        func = getattr(client, method)
        self.response = func(url, request_data, format='json', **kwargs)
        with self.subTest():
            self.assertEqual(exp_status, self.response.status_code)

        if exp_response_data == ():
            return None

        response_data = self.response.json()
        with self.subTest():
            self.assertEqual(exp_response_data, response_data)
        return response_data
