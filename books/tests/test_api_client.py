from random import randint

from books.requests.api_client import login


class TestApiClient:
    nr = randint(1, 9999999999)
    clientName = 'Maria'
    clientEmail = f'valid_email{nr}@email.com'

    def setup_method(self):
        self.response = login(self.clientName, self.clientEmail)

    def test_login_200(self):
        assert self.response.status_code == 201, 'Status code is not OK!'

    def test_login_has_token_key(self):
        assert 'accessToken' in self.response.json().keys(), 'Token key is not present!'

    def test_login_409(self):
        self.response = login(self.clientName, self.clientEmail)
        assert self.response.status_code == 409, 'Status code is not OK!'
        assert self.response.json()[
                   'error'] == 'API client already registered. Try a different email.', 'Existing user message not OK!'

    def test_invalid_email(self):
        self.response = login('Maria', 'abc')
        assert self.response.status_code == 400, 'Status code is not OK!'
        assert self.response.json()[
                   'error'] == 'Invalid or missing client email.', 'Invalid email error is not correct!'
