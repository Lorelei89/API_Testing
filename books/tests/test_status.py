import sys

import pytest

from books.requests.status import *


class TestStatus:

    def test_status_200(self):
        assert get_status().status_code == 200, 'Status code is not OK!'
        assert get_status().json()['status'] == 'OK', 'Status message is not OK!'


if __name__ == '__main__':
    sys.exit(pytest.main(["-qq"], plugins=[TestStatus()]))

