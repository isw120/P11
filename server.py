import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime, timedelta


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def checkEmail(email):
    try:
        club = [club for club in clubs if club['email'] == email][0]
        return club
    except IndexError:
        raise IndexError()

def checkAvailablePoints(competitionParam, clubParam, placesParam):
    competition = [c for c in competitions if c['name'] == competitionParam][0]
    club = [c for c in clubs if c['name'] == clubParam][0]
    placesRequired = int(placesParam)
    if (placesRequired * 3) <= int(club['points']):
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['points'] = int(club['points']) - (placesRequired * 3)
        check = False
        return check, club, competition
    else:
        check = True
        return check, clubParam, competitionParam

def checkCompetitionsDates():
    all_competitions = []
    today = datetime.now()
    for c in competitions:
        competition_date = datetime.strptime(c['date'], '%Y-%m-%d %H:%M:%S')
        if today < competition_date:
            c['status'] = 'valid'
        else:
            c['status'] = 'invalid'
        all_competitions.append(c)
    return all_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
        try:
            club = checkEmail(request.form['email'])
            other_clubs = [c for c in clubs if c['email'] != request.form['email']]
            all_competitions = checkCompetitionsDates()
            return render_template('welcome.html', club=club, clubs=other_clubs, competitions=all_competitions)
        except IndexError:
            return render_template('index.html', error="Sorry, that email wasn't found.")


@app.route('/book/<competition>/<club>')
def book(competition,club, error=None):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    other_clubs = [c for c in clubs if c['name'] != club]
    if error is not None:
        return render_template('booking.html',club=foundClub,competition=foundCompetition, error=error)
    if foundCompetition['status'] == 'invalid':
        flash("The competition " + str(foundCompetition['name']) + " is invalid.")
        return render_template('welcome.html', club=foundClub, clubs=other_clubs, competitions=competitions)
    if foundCompetition['numberOfPlaces'] == 0:
        flash("The competition " + str(foundCompetition['name']) + " is completed.")
        return render_template('welcome.html', club=foundClub, clubs=other_clubs, competitions=competitions)
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=foundClub, clubs=other_clubs, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    if int(request.form['places']) > 12:
        return book(request.form['competition'], request.form['club'], "You cant book more than 12 places")
    check, club, competition = checkAvailablePoints(request.form['competition'], request.form['club'], request.form['places'])
    other_clubs = [c for c in clubs if c['name'] != request.form['club']]
    if check is False:
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, clubs=other_clubs, competitions=competitions)
    else:
        return book(competition, club, "You dont have enough points")


# TODO: Add route for points display
@app.route('/displayPoints')
def displayPoints():
        return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))