import unittest

import pytest, requests

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

    def test_index_url(self):
        assert 200 == requests.get('http://127.0.0.1:5000').status_code

    def test_showSummary_url(self):
        assert 200 == requests.post("http://localhost:5000/showSummary", {"email": "john@simplylift.co"}).status_code

    def test_book_url(self):
        assert 200 == requests.get("http://localhost:5000/book/Spring%20Festival/Simply%20Lift").status_code

    def test_purchasePlaces_url(self):
        assert 200 == requests.post("http://localhost:5000/purchasePlaces", {"club": "Simply Lift", "competition": "Spring Festival", "places": "3"}).status_code

    def test_logout_url(self):
        assert 200 == requests.get("http://localhost:5000/logout").status_code


if __name__ == '__main__':
    unittest.main()