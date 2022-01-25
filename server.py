import json
from flask import Flask,render_template,request,redirect,flash,url_for


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
    if placesRequired <= int(club['points']):
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['points'] = int(club['points']) - placesRequired
        check = False
        return check, club, competition
    else:
        check = True
        return check, clubParam, competitionParam




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
            return render_template('welcome.html', club=club, competitions=competitions)
        except IndexError:
            return render_template('index.html', error="Sorry, that email wasn't found.")


@app.route('/book/<competition>/<club>')
def book(competition,club, error=None):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if error is not None:
        return render_template('booking.html',club=foundClub,competition=foundCompetition, error=error)
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    check, club, competition = checkAvailablePoints(request.form['competition'], request.form['club'], request.form['places'])
    if check is False:
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        return book(competition, club, "You dont have enough points")


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))