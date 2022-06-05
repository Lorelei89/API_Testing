import sys

import pytest

from books.requests.api_client import get_token
from books.requests.orders import add_order, delete_order, get_orders, get_order, edit_order


class TestOrders:
    def setup_method(self):
        self.token = get_token()

    def test_add_order_book_out_of_stock(self):
        r = add_order(self.token, 2, 'Maria')
        assert r.status_code == 404, 'code not ok'
        assert r.json()['error'] == 'This book is not in stock. Try again later.', 'error not ok'

    def test_add_valid_order(self):
        r = add_order(self.token, 1, 'Maria')
        assert r.status_code == 201, 'code not ok'
        assert r.json()['created'] is True, 'order not created'
        delete_order(self.token, r.json()['orderId'])

    def test_get_orders(self):
        add1 = add_order(self.token, 1, 'Maria')
        add2 = add_order(self.token, 3, 'Maria')
        r = get_orders(self.token)
        assert r.status_code == 200, 'Code not OK'
        assert len(r.json()) == 2, 'Get orders not working'
        delete_order(self.token, add1.json()['orderId'])
        delete_order(self.token, add2.json()['orderId'])

    def test_delete_order(self):
        add = add_order(self.token, 1, 'Maria')
        r = delete_order(self.token, add.json()['orderId'])
        assert r.status_code == 204, 'Code not OK'
        get_all = get_orders(self.token)
        assert len(get_all.json()) == 0, 'Order was not deleted'

    def test_delete_invalid_order_id(self):
        r = delete_order(self.token, '123abc')
        assert r.status_code == 404, 'Code not OK'
        assert r.json()['error'] == 'No order with id 123abc.', 'Error not Ok'

    def test_get_order(self):
        id = add_order(self.token, 1, 'Maria').json()['orderId']
        r = get_order(self.token, id)
        assert r.status_code == 200, 'Code not OK'
        assert r.json()['id'] == id, 'ID not OK'
        assert r.json()['bookId'] == 1, 'BookID not OK'
        assert r.json()['customerName'] == 'Maria', 'Customer name not OK'
        assert r.json()['quantity'] == 1, 'Quantity not OK'
        delete_order(self.token, id)

    def test_get_invalid_order_id(self):
        r = get_order(self.token, '123qwe')
        assert r.status_code == 404, 'Code not OK'
        assert r.json()['error'] == 'No order with id 123qwe.', 'Error message not OK'

    def test_get_order_invalid_token(self):
        r = get_order('123', '123abc')
        assert r.status_code == 401, 'Code not OK'
        assert r.json()['error'] == 'Invalid bearer token.', 'Error message not OK'

    def test_patch_invalid_order(self):
        r = edit_order(self.token, '123abc', 'Maria2')
        assert r.status_code == 404, 'Code not OK'
        assert r.json()['error'] == 'No order with id 123abc.', 'Error message not correct'

    def test_patch_invalid_order_id(self):
        id = add_order(self.token, 1, 'Maria').json()['orderId']
        r = edit_order(self.token, id, 'Andreea')
        assert r.status_code == 204, 'Code not Ok'
        get = get_order(self.token, id)
        assert get.json()['customerName'] == 'Andreea', 'Update name not working'
        delete_order(self.token, id)


if __name__ == '__main__':
    sys.exit(pytest.main(["-qq"], plugins=[TestOrders()]))

