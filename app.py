# Name: app.py
# Description: Main app for Meeting API, an api for a meeting scheduler.
#              Please install requirements in requirements.txt first. (not created yet)

from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap


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

if __name__ == '__main__':
    Bootstrap(app)
    app.secret_key = 'devkey'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'
    app.run(debug=True, host='0.0.0.0')
