import unittest

import pytest

from server import checkEmail, checkAvailablePoints


class TestApp(unittest.TestCase):

    def test_email_not_found(self):
        with pytest.raises(IndexError):
            checkEmail("email@email.fr")

    def test_email_found(self):
        club = checkEmail("john@simplylift.co")
        assert club['name'] == 'Simply Lift'

    def test_purchase_places_success(self):
        check, club, competition = checkAvailablePoints("Spring Festival", "Simply Lift", 5)
        assert check == False

    def test_purchase_places_failure(self):
        check, club, competition = checkAvailablePoints("Spring Festival", "Simply Lift", 30)
        assert check == True

if __name__ == '__main__':
    unittest.main()