import unittest

import pytest

from server import checkEmail, checkAvailablePoints, checkCompetitionsDates


class TestApp(unittest.TestCase):

    def test_email_not_found(self):
        with pytest.raises(IndexError):
            checkEmail("email@email.fr")

    def test_email_found(self):
        club = checkEmail("john@simplylift.co")
        assert club['name'] == 'Simply Lift'

    def test_purchase_places_success(self):
        check, club, competition = checkAvailablePoints("Spring Festival", "Simply Lift", 2)
        assert check == False

    def test_purchase_places_failure(self):
        check, club, competition = checkAvailablePoints("Spring Festival", "Simply Lift", 30)
        assert check == True

    def test_places_correctly_deducted_from_competition(self):
        check, club, competition = checkAvailablePoints("Spring Festival", "Simply Lift", 2)
        assert check == False
        assert competition['numberOfPlaces'] == 23

    def test_competitions_dates(self):
        all_competitions = checkCompetitionsDates()
        competition_01 = all_competitions[0]
        competition_02 = all_competitions[2]
        assert competition_01['status'] == 'invalid'
        assert competition_02['status'] == 'valid'

if __name__ == '__main__':
    unittest.main()