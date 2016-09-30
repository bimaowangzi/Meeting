# Name: app.py
# Description: Main app for Meeting API, an api for a meeting scheduler.
#              Please install requirements in requirements.txt first. (not created yet)

from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
import sqlite3 as lite


app = Flask(__name__)
#TODO: sqlite implementation, use local dict first


@app.route('/')
def api_root():
    #TODO: not sure if you want to show lists of everything here. if not we can just leave this.
    return render_template('index.html')

@app.route('/meeting')
def api_meetings():
    #TODO: GET - show list of meetings.
    return 'List of meetings: ' + url_for('api_meetings')

@app.route('/meeting/<m_id>')
def api_meeting(m_id):
    #TODO: GET - show details of specific meeting. PUT - edit meeting details. DELETE - remove meeting. POST - create new meeting.
    return 'You are at meeting ' + m_id

@app.route('/person')
def api_persons():
    #TODO: GET - show list of persons
    return 'List of persons: ' + url_for('api_persons')

@app.route('/person/<p_id>')
def api_person(p_id):
    #TODO: GET - show details of specific person. POST - create new person. PUT - edit person details. DELETE - delete person.
    return 'You are at person ' + p_id

def refresh_sqlite_database(db):
    # Refreshes the sqlite database.
    con = lite.connect(db)
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Person")
        cur.execute("DROP TABLE IF EXISTS Meeting")
        cur.execute("DROP TABLE IF EXISTS Schedules")
        cur.execute('CREATE TABLE Person(p_id INT, name TEXT, timetable TEXT)')
        cur.execute('CREATE TABLE Meeting(m_id INT, start_time TEXT, end_time TEXT, location TEXT)') # should we consider using a standardised format (e.g. like person's timetable?)
        cur.execute('CREATE TABLE Schedules(m_id INT, p_id TEXT)')


def insert_sample_data(db):
    con = lite.connect(db)
    with con:
        curs = con.cursor()
        persons = (
            (1, 'Shaun', "1300-1500, 1800-2100"),
            (2, 'Junsheng', ""),
            (3, 'Sam', "1000-1100"),
            (4, 'Ryan', "2200-2400"),
            (5, 'Hazel', "900-1800"),
            (6, 'Junqi', "100-200, 400-600, 800-1000, 1400-1600"),
            (7, 'Bella', "1230-2300")
        )
        meetings = (
            (1, "1030", "1200", "Shauns Room"),
        )
        schedules = (
            (1, 1),
            (1, 2),
            (1, 7)
        )
        curs.executemany("INSERT INTO Person VALUES(?, ?, ?)", persons)
        curs.executemany("INSERT INTO Meeting VALUES(?, ?, ?, ?)", meetings)
        curs.executemany("INSERT INTO Schedules VALUES(?, ?)", schedules)

def get_state_of_db(db, table):
    con = lite.connect(db)
    with con:
        curs = con.cursor()
        curs.execute("SELECT * FROM {0}".format(table))
        rows = curs.fetchall()
        for row in rows:
            print(row)


if __name__ == '__main__':
    refresh_sqlite_database('test.db')
    insert_sample_data('test.db')
    get_state_of_db('test.db', "Person")
    Bootstrap(app)
    app.secret_key = 'devkey'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'
    app.run(debug=True, host='0.0.0.0')
