# Name: app.py
# Description: Main app for Meeting API, an api for a meeting scheduler.
#              Please install requirements in requirements.txt first. (not created yet)

from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
import sqlite3 as lite
from functools import wraps
from flask import json
from flask import jsonify

db = 'test.db'
app = Flask(__name__)

def check_auth(username, password):
    return username == 'admin' and password == 'password'

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

#RESTful flask tutorial: http://blog.luisrei.com/articles/flaskrest.html
@app.route('/')
def api_root():
    global db
    return render_template('index.html', list_of_persons=get_state_of_db(db, "Person"), list_of_meetings=get_state_of_db(db, "Meeting"), list_of_schedules=get_state_of_db(db, "Schedules"))

@app.route('/meeting', methods = ['GET'])
@requires_auth
def api_meetings():
    try:
        con = lite.connect(db)
        with con:
            curs = con.cursor()
            curs.execute("SELECT * FROM {0}".format("Meeting"))
            rows = curs.fetchall()
            meetingJson = {}
            for row in rows:
                # cur.execute('CREATE TABLE Meeting(m_id INT PRIMARY KEY, start_time TEXT, end_time TEXT, location TEXT)')
                data = {}
                data['start_time'] = row[1]
                data['end_time'] = row[2]
                data['location'] = row[3]
                meetingJson[row[0]] = data
            returnJson = json.dumps(meetingJson)
    except Exception as e:
        return not_found()
    return 'GET /meeting\n' + returnJson

@app.route('/meeting/<m_id>', methods = ['GET', 'PUT', 'DELETE', 'POST'])
@requires_auth
def api_meeting(m_id):
    #TODO: PUT - edit meeting details. DELETE - remove meeting.
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
        return 'DELETE: You have successfully deleted meeting ' + m_id


@app.route('/person', methods = ['GET'])
@requires_auth
def api_persons():
    try:
        con = lite.connect(db)
        with con:
            curs = con.cursor()
            curs.execute("SELECT * FROM {0}".format("Person"))
            rows = curs.fetchall()
            personJson = {}
            for row in rows:
                # cur.execute('CREATE TABLE Meeting(m_id INT PRIMARY KEY, start_time TEXT, end_time TEXT, location TEXT)')
                data = {}
                data['name'] = row[1]
                data['timetable'] = row[2]
                personJson[row[0]] = data
            returnJson = json.dumps(personJson)
    except Exception as e:
        return not_found()
    return 'GET /person\n' + returnJson

@app.route('/person/<p_id>', methods = ['GET', 'PUT', 'DELETE', 'POST'])
@requires_auth
def api_person(p_id):
    #TODO: POST - create new person. PUT - edit person details.
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
        con = lite.connect(db)
        with con:
            curs = con.cursor()
            try:
                curs.execute("DELETE FROM Person WHERE p_id={0}".format(p_id))
            except Exception as e:
                returnText ="An error occurred: " +  e.args[0]
        return 'DELETE: You have successfully deleted person ' + p_id

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.errorhandler(409)
def conflict(error=None):
    message = {
        'status': 409,
        'message': 'Conflict: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 409

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
            (1, 7),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            (2, 5),
            (2, 6),
            (2, 7)
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
        return rows

if __name__ == '__main__':
    refresh_sqlite_database(db)
    insert_sample_data(db)
    #get_state_of_db(db, "Person")
    Bootstrap(app)
    app.secret_key = 'devkey'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'
    app.run(debug=True, host='0.0.0.0')
