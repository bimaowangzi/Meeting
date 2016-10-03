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
def api_meetings():
    return GET_Meetings()

@app.route('/meeting/<m_id>', methods = ['GET', 'PUT', 'DELETE', 'POST'])
@requires_auth
def api_meeting(m_id):
    con = lite.connect(db)
    #TODO: PUT - edit meeting details. POST - create meeting.
    if request.method == 'GET':
        # Look up meeting m_id in Meeting
        with con:
            curs = con.cursor()
            try:
                curs.execute("SELECT * FROM Meeting WHERE m_id={0}".format(m_id))
                rows = curs.fetchall()
                if len(rows) == 0:
                    return not_found("This m_id does not exist.")
                else:
                    MeetingRow = rows[0]
                    returnText = "GET: /meeting/{0}\nStart Time: {1}\nEnd Time: {2}\nLocation: {3}".format(m_id, MeetingRow[1], MeetingRow[2], MeetingRow[3])
            except Exception as e:
                return not_found("Something went wrong during GET.")
                # returnText = "An error occurred: " +  e.args[0]
        return returnText

    elif request.method == 'POST':
        with con:
            curs = con.cursor()
            try:
                if verify_existence_meeting(curs, m_id): #if it exists, this is a conflict
                    return conflict("This m_id already exists. Use PUT to create new meeting.")
                else: # we can add it
                    #TODO: check valid meeting before adding

                    curs.execute("INSERT INTO Meeting VALUES({0}, '{1}', '{2}', '{3}')".format(int(m_id), request.args['start_time'], request.args['end_time'], request.args['location']))
                    con.commit()
                    return "POST: Successful"
            except:
                return not_found("Something went wrong during POST.")
    elif request.method == 'PUT':
        with con:
            curs = con.cursor()
            try:
                if verify_existence_meeting(curs, m_id):  # if it exists, this is a conflict
                    # TODO: check valid meeting before putting
                    curs.execute("UPDATE Meeting SET start_time=? WHERE m_id=?", (request.args['start_time'], m_id))
                    curs.execute("UPDATE Meeting SET end_time=? WHERE m_id=?", (request.args['end_time'], m_id))
                    curs.execute("UPDATE Meeting SET location=? WHERE m_id=?", (request.args['location'], m_id))
                    con.commit()
                    return "PUT: Successful"
                else:  # not found
                    return not_found("This m_id does not exist.")

            except:
                return not_found("Something went wrong during PUT.")

    elif request.method == 'DELETE':
        with con:
            curs = con.cursor()
            if (verify_existence_meeting(curs, m_id)): #if we verify that the person exists, try delete
                try:
                    curs.execute("DELETE FROM Meeting WHERE m_id={0}".format(m_id))
                except Exception as e:
                    return not_found("Something went wrong during DELETE.")
            else:
                return not_found("This m_id does not exist.")
        return 'DELETE: You have successfully deleted meeting ' + m_id

# the checking is not working ...
def verify_existence_schedule(curs, m_id, p_id):
    # verifies that schedule exists, given curs (sqlite cursor) m_id.
    curs.execute("SELECT 1 FROM Schedules WHERE m_id = {0} AND p_id = {1}".format(m_id,p_id))
    if curs.fetchone():
        return True
    return False

def verify_existence_meeting(curs, m_id):
    # verifies that a meeting exists, given curs (sqlite cursor) m_id.
    curs.execute("SELECT 1 FROM Meeting WHERE m_id = {0}".format(m_id))
    if curs.fetchone():
        return True
    return False


def verify_existence_person(curs, p_id):
    #verifies that a person exists, given curs (sqlite cursor) and p_id.
    curs.execute("SELECT 1 FROM Person WHERE p_id = {0}".format(p_id))
    if curs.fetchone():
        return True
    return False

def GET_Meetings():
    try:
        con = lite.connect(db)
        with con:
            curs = con.cursor()
            curs.execute("SELECT * FROM {0}".format("Meeting"))
            rows = curs.fetchall()
            if (request.headers["content-type"] == "application/json"):
                meetingJson = {}
                for row in rows:
                    # cur.execute('CREATE TABLE Meeting(m_id INT PRIMARY KEY, start_time TEXT, end_time TEXT, location TEXT)')
                    data = {}
                    data['start_time'] = row[1]
                    data['end_time'] = row[2]
                    data['location'] = row[3]
                    meetingJson[row[0]] = data
                return 'GET /meeting\n' + json.dumps(meetingJson)
            else:
                returnText = 'GET /meeting\n\n'
                for row in rows:
                    # cur.execute('CREATE TABLE Meeting(m_id INT PRIMARY KEY, start_time TEXT, end_time TEXT, location TEXT)')
                    meeting = "Start Time: {0}\nEnd Time: {1}\nLocation: {2}\n\n".format(row[1],row[2],row[3])
                    returnText += meeting
                return returnText
    except Exception as e:
        return e.args[0]
        # return not_found()

def GET_Persons():
    try:
        con = lite.connect(db)
        with con:
            curs = con.cursor()
            curs.execute("SELECT * FROM {0}".format("Person"))
            rows = curs.fetchall()
            if (request.headers["content-type"] == "application/json"):
                personJson = {}
                for row in rows:
                    # cur.execute('CREATE TABLE Meeting(m_id INT PRIMARY KEY, start_time TEXT, end_time TEXT, location TEXT)')
                    data = {}
                    data['name'] = row[1]
                    data['timetable'] = row[2]
                    personJson[row[0]] = data
                return 'GET /person\n' + json.dumps(personJson)
            else:
                returnText = 'GET /person\n\n'
                for row in rows:
                    # cur.execute('CREATE TABLE Meeting(m_id INT PRIMARY KEY, start_time TEXT, end_time TEXT, location TEXT)')
                    person = "Name: {0}\nTimetable: {1}\n\n".format(row[1],row[2])
                    returnText += person
                return returnText
    except Exception as e:
        return not_found()

@app.route('/person', methods = ['GET'])
def api_persons():
    return GET_Persons()

@app.route('/person/<p_id>', methods = ['GET', 'PUT', 'DELETE', 'POST'])
@requires_auth
def api_person(p_id):
    con = lite.connect(db)
    #TODO: POST - create new person. PUT - edit person details.
    if request.method == 'GET':
        # Look up person p_id in Person
        with con:
            curs = con.cursor()
            try:
                curs.execute("SELECT * FROM Person WHERE p_id={0}".format(p_id))
                rows = curs.fetchall()
                if len(rows) == 0:
                    return not_found("This p_id is not found.")
                    # returnText = "GET: /person/{0} NOT FOUND.".format(p_id)
                else:
                    PersonRow = rows[0]
                    returnText = "GET: /person/{0}\nName: {1}\nSchedule: {2}".format(p_id, PersonRow[1], PersonRow[2])
            except Exception as e:
                return not_found("Something went wrong during GET.")
                # returnText ="GET: /person/{0} NOT FOUND {1}".format(p_id,e.args[0])
        return returnText
    elif request.method == 'POST':
        with con:
            curs = con.cursor()
            try:
                if verify_existence_person(curs, p_id):  # if it exists, this is a conflict
                    return conflict("This p_id already exists.")
                else:  # we can add it
                    curs.execute("INSERT INTO Person VALUES({0}, '{1}', '""')".format(int(p_id), request.args['name']))
                    con.commit()
                    return "POST /person/: Successful"
            except:
                return not_found("Something went wrong during POST.")
    elif request.method == 'PUT':
        with con:
            curs = con.cursor()
            try:
                if verify_existence_person(curs, p_id):   # we can put it
                    curs.execute("UPDATE Person SET name=? WHERE p_id=?", (request.args['name'],p_id))
                    con.commit()
                    return "PUT /person/: Successful"
                else:
                    return not_found("This person doesn't exist. Use POST to create a new one.")
            except:
                return not_found("Something went wrong during PUT.")
    elif request.method == 'DELETE':
        with con:
            curs = con.cursor()
            if (verify_existence_person(curs, p_id)): #if we verify that the person exists, try delete
                try:
                    curs.execute("DELETE FROM Person WHERE p_id={0}".format(p_id))
                except Exception as e:
                    return not_found("Something went wrong in deleting.")
            else:
                return not_found("This p_id does not exist.")
        return 'DELETE: You have successfully deleted person ' + p_id

@app.route('/schedule', methods = ['GET', 'POST', 'DELETE'])
@requires_auth
def api_schedule():
    con = lite.connect(db)
    if request.method == 'GET':
        try:
            with con:
                curs = con.cursor()
                curs.execute("SELECT * FROM {0}".format("Schedules"))
                rows = curs.fetchall()
                ScheduleJson = {}
                count = 0
                for row in rows:
                    # (m_id INT, p_id TEXT,
                    data = {}
                    data['m_id'] = row[0]
                    data['p_id'] = row[1]
                    ScheduleJson[count] = data
                    count+=1
                returnJson = json.dumps(ScheduleJson)
        except Exception as e:
            return not_found("Something went wrong with GET.")
        return 'GET /schedule\n' + returnJson
    elif request.method == 'POST':
        with con:
            curs = con.cursor()
            try:
                if verify_existence_schedule(curs, request.args['m_id'], request.args['p_id']):  # if it exists, this is a conflict
                    return conflict("This meeting already exists.")
                elif verify_existence_person(curs, request.args['p_id']) == False:  # if p_id does not exists, this is a conflict
                    return conflict("This p_id does not exist.")
                elif verify_existence_meeting(curs, request.args['m_id']) == False:  # if m_id does not exists, this is a conflict
                    return conflict("This m_id does not exist.")
                else:  # we can add it
                    # TODO: check valid schedule before adding
                    # fetch the meeting time
                    curs.execute("SELECT start_time, end_time FROM Meeting WHERE m_id={0}".format(request.args['m_id']))
                    meetingrows= curs.fetchone()
                    # fetch timetable of person
                    curs.execute("SELECT timetable FROM Person WHERE p_id={0}".format(request.args['p_id']))
                    personrows = curs.fetchone()[0]
                    split_persons = personrows.split(", ")
                    # do a comparison
                    for busy_period in split_persons:
                        start_time_busy, end_time_busy = busy_period.strip().split("-")
                        if start_time_busy<meetingrows[0] and end_time_busy>meetingrows[0]: #if meeting starts within a busy time,
                            return conflict("Meeting starts within busy time {0}".format(busy_period))
                        elif start_time_busy<meetingrows[1] and end_time_busy>meetingrows[1]: #elif meeting ends within a busy time,
                            return conflict("Meeting ends within busy time {0}".format(busy_period))
                        elif start_time_busy>meetingrows[0] and end_time_busy<meetingrows[1]: #elif meeting encapsulates a busy time,
                            return conflict("Meeting encapsultates a busy time {0}".format(busy_period))
                    curs.execute("INSERT INTO Schedules VALUES({0}, {1})".format(request.args['m_id'],request.args['p_id']))
                    split_persons.append("{0}-{1}".format(meetingrows[0],meetingrows[1]))
                    split_persons.sort()
                    con.execute("UPDATE Person SET timetable=? WHERE p_id=?", (str(split_persons), request.args['p_id']))
                    con.commit()
                    return "You have successfully insert person {0}\'s schedule for meeting {1}.".format(request.args['p_id'],request.args['m_id'])
            except Exception as e:
                return not_found("Something went wrong while POSTing. "+e.args[0])
    elif request.method == 'DELETE':
        with con:
            curs = con.cursor()
            if verify_existence_schedule(curs, request.args['m_id'], request.args['p_id']): #if we verify that the person exists, try delete
                try:
                    curs.execute("DELETE FROM Schedules WHERE m_id={0} AND p_id={1}".format(request.args['m_id'],request.args['p_id']))
                    curs.execute("SELECT start_time, end_time FROM Meeting WHERE m_id={0}".format(request.args['m_id']))
                    meetingrows = curs.fetchone()
                    start_time, end_time = meetingrows
                    curs.execute("SELECT timetable FROM Person WHERE p_id={0}".format(request.args['p_id']))
                    personrows = curs.fetchone()[0]
                    split_persons = personrows[1:-1].split(", ")
                    for time in split_persons:
                        if start_time in time:
                            if end_time in time:
                                split_persons.remove(time)
                    timetable_string = ""
                    for element in split_persons:
                        timetable_string+=element[1:-1]+", "
                    con.execute("UPDATE Person SET timetable=? WHERE p_id=?", (timetable_string[:-2], request.args['p_id']))
                    con.commit()
                    return "Successful deletion of schedule {0}".format(time)

                except Exception as e:
                    return not_found("Something went wrong when deleting that. "+e.args[0])
            else:
                return not_found("Can't find a person with that m_id.")
        return "DELETE: You have successfully deleted person {0}\'s schedule for meeting {1}.".format(request.args['p_id'],request.args['m_id'])

@app.errorhandler(404)
def not_found(error=None):
    if error==None:
        message = {
                'status': 404,
                'message': 'Not Found: ' + request.url,
        }
    else:
        message = {
            'status': 404,
            'message': 'Not Found: ' + request.url + " Error: " + error,
        }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.errorhandler(409)
def conflict(error=None):
    if error==None:
        message = {
            'status': 409,
            'message': 'Conflict: ' + request.url,
        }
    else:
        message = {
            'status': 409,
            'message': 'Conflict: ' + request.url +" Error: " + error,
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
        cur.execute('CREATE TABLE Schedules(m_id INT, p_id TEXT, PRIMARY KEY(m_id, p_id), FOREIGN KEY(m_id) REFERENCES Meeting, FOREIGN KEY(p_id) REFERENCES Person)')

def insert_sample_data(db):
    #inserts some sample database into the database.
    #takes in database name (db).
    con = lite.connect(db)
    with con:
        curs = con.cursor()
        # persons = (
        #     (1, 'Shaun', "1300-1500, 1800-2100"),
        #     (2, 'Junsheng', ""),
        #     (3, 'Sam', "1000-1100"),
        #     (4, 'Ryan', "2200-2400"),
        #     (5, 'Hazel', "900-1800"),
        #     (6, 'Junqi', "100-200, 400-600, 800-1000, 1400-1600"),
        #     (7, 'Bella', "1230-2300")
        # )
        # meetings = (
        #     (1, "1030", "1200", "Shauns Room"),
        #     (2, "1400", "1600", "Canteen"),
        # )
        # schedules = (
        #     (1, 1),
        #     (1, 2),
        #     (1, 7),
        #     (2, 1),
        #     (2, 2),
        #     (2, 3),
        #     (2, 4),
        #     (2, 5),
        #     (2, 6),
        #     (2, 7)
        # )
        persons = (
            (1, 'Shaun', "1030-1200, 1400-1600"),
            (2, 'Junsheng', "1030-1200, 1800-2100")
        )
        meetings = (
            (1, "1030", "1200", "Shauns Room"),
            (2, "1400", "1600", "Canteen"),
            (3, "1800", "2100", "Changi City Point"),
            (4, "0800", "1000", "Conflict Room")
        )
        schedules = (
            (1, 1),
            (1, 2),
            (2, 1),
            (3, 2)
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
