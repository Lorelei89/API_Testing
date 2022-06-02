from books.requests.books import *


class TestBooks:
    def test_get_books_200(self):
        r = get_books()
        assert r.status_code == 200, 'Status code is not OK!'

    def test_get_books_invalid_type(self):
        r = get_books(book_type='abc')
        assert r.status_code == 400, 'Status code is not OK!'
        print(r.json())
        assert r.json()['error'] == "Invalid value for query parameter 'type'. Must be one of: fiction, non-fiction."

    def test_get_all_books(self):
        r = get_books()
        assert len(r.josn()) == 6, "Book total is wrong"

    def test_get_all_books_limit(self):
        r = get_books(limit=3)
        assert len(r.json()) == 3, 'Limit is not working.'

    def test_get_all_books_type_fiction(self):
        r = get_books(book_type='fiction')
        assert len(r.json()) == 4, 'Type fiction is not working.'

    def test_get_all_books_type_non_fiction(self):
        r = get_books(book_type='non-fictional')
        assert len(r.json()) == 2, 'Type non-fiction is not working.'

    def test_get_all_books_type_limit(self):
        r = get_books(book_type='fiction', limit=2)
        assert len(r.json()) == 2, 'Limit are not working!'
        assert r.json()[0]['type'] == 'fiction', 'Type filter is not working.'
        assert r.json()[1]['type'] == 'non-fiction', 'Type filter is not working.'

    def test_get_book(self):
        r = get_book(1)
        expected = {
            'author': 'James Patterson and James O. Born',
            'available': True,
            'current-stock': 12,
            'id': 1,
            'isbn': '1780899475',
            'name': 'The Russian',
            'price': 12.98,
            'type': 'fiction'
        }
        assert r.status_code == 200, 'Status code is not OK'
        assert r.json() == expected, 'Book data is not OK'

    def test_get_book_invalid_id(self):
        r = get_book(202)
        assert r.status_code == 404, 'Status code is not OK'
        assert r.json()['error'] == 'No book with id 202', 'Invalid ID message not OK'
