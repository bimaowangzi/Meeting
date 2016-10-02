# Name: app.py
# Description: Main app for Meeting API, an api for a meeting scheduler.
#              Please install requirements in requirements.txt first. (not created yet)

from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
import sqlite3 as lite

from flask import jsonify

db = 'test.db'
app = Flask(__name__)

#TODO: add user authentication for something

#RESTful flask tutorial: http://blog.luisrei.com/articles/flaskrest.html
@app.route('/')
def api_root():
    #TODO: not sure if you want to show lists of everything here. if not we can just leave this.
    return render_template('index.html')

@app.route('/meeting', methods = ['GET'])
def api_meetings():
    #TODO: GET - show list of meetings.
    return 'List of meetings: ' + url_for('api_meetings')

@app.route('/meeting/<m_id>', methods = ['GET', 'PUT', 'DELETE', 'POST'])
def api_meeting(m_id):
    #TODO: GET - show details of specific meeting. PUT - edit meeting details. DELETE - remove meeting. POST - create new meeting.
    if request.method == 'GET':
        # Look up meeting m_id in Meeting
        con = lite.connect(db)
        with con:
            curs = con.cursor()
            try:
                curs.execute("SELECT * FROM Meeting WHERE m_id={0}".format(m_id))
                rows = curs.fetchall()
                if len(rows) == 0:
                    return not_found()
                else:
                    MeetingRow = rows[0]
                    returnText = "GET: /meeting/{0}\nStart Time: {1}\nEnd Time: {2}\nLocation: {3}".format(m_id, MeetingRow[1], MeetingRow[2], MeetingRow[3])
            except Exception as e:
                return not_found()
                # returnText = "An error occurred: " +  e.args[0]
        return returnText
    elif request.method == 'POST':
        return 'POST: You are at meeting ' + m_id
    elif request.method == 'PUT':
        return 'PUT: You are at meeting ' + m_id
    elif request.method == 'DELETE':
        con = lite.connect(db)
        with con:
            curs = con.cursor()
            try:
                curs.execute("DELETE FROM Meeting WHERE m_id={0}".format(m_id))
            except Exception as e:
                returnText ="An error occurred: " +  e.args[0]
        return 'You have successfully deleted meeting ' + m_id


@app.route('/person', methods = ['GET'])
def api_persons():
    #TODO: GET - show list of persons
    return 'List of persons: ' + url_for('api_persons')

@app.route('/person/<p_id>', methods = ['GET', 'PUT', 'DELETE', 'POST'])
def api_person(p_id):
    #TODO: GET - show details of specific person. POST - create new person. PUT - edit person details. DELETE - delete person.
    if request.method == 'GET':
        # Look up person p_id in Person
        con = lite.connect(db)
        with con:
            curs = con.cursor()
            try:
                curs.execute("SELECT * FROM Person WHERE p_id={0}".format(p_id))
                rows = curs.fetchall()
                if len(rows) == 0:
                    return not_found()
                    # returnText = "GET: /person/{0} NOT FOUND.".format(p_id)
                else:
                    PersonRow = rows[0]
                    returnText = "GET: /person/{0}\nName: {1}\nSchedule: {2}".format(p_id, PersonRow[1], PersonRow[2])
            except Exception as e:
                return not_found()
                # returnText ="GET: /person/{0} NOT FOUND {1}".format(p_id,e.args[0])
        return returnText
    elif request.method == 'POST':
        return 'POST: You are at person ' + p_id
    elif request.method == 'PUT':
        return 'PUT: You are at person ' + p_id
    elif request.method == 'DELETE':
        return 'DELETE: You are at person ' + p_id

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

def refresh_sqlite_database(db):
    # Refreshes the sqlite database.
    con = lite.connect(db)
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Person")
        cur.execute("DROP TABLE IF EXISTS Meeting")
        cur.execute("DROP TABLE IF EXISTS Schedules")
        cur.execute('CREATE TABLE Person(p_id INT PRIMARY KEY, name TEXT, timetable TEXT)')
        cur.execute('CREATE TABLE Meeting(m_id INT PRIMARY KEY, start_time TEXT, end_time TEXT, location TEXT)') # should we consider using a standardised format (e.g. like person's timetable?)
        cur.execute('CREATE TABLE Schedules(m_id INT, p_id TEXT, PRIMARY KEY(m_id, p_id))')


def insert_sample_data(db):
    #inserts some sample database into the database.
    #takes in database name (db).
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
            (2, "1400", "1600", "Canteen"),
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
    # prints state of db.
    # takes in database name (db), and table to print (table).
    con = lite.connect(db)
    with con:
        curs = con.cursor()
        curs.execute("SELECT * FROM {0}".format(table))
        rows = curs.fetchall()
        for row in rows:
            print(row)

if __name__ == '__main__':
    refresh_sqlite_database(db)
    insert_sample_data(db)
    get_state_of_db(db, "Person")
    Bootstrap(app)
    app.secret_key = 'devkey'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'
    app.run(debug=True, host='0.0.0.0')
