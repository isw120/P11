import unittest

import pytest

from server import checkEmail

class TestApp(unittest.TestCase):

    def test_email_not_found(self):
        with pytest.raises(IndexError):
            checkEmail("email@email.fr")

    def test_email_found(self):
        club = checkEmail("john@simplylift.co")
        assert club['name'] == 'Simply Lift'

if __name__ == '__main__':
    unittest.main()