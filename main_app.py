from flask import Flask, render_template, session, send_from_directory
from uuid import uuid4
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='static', template_folder='templates')

app.secret_key = "ThisJustHasToBeARandomStringOfCharacters"

placement = 0
placementDict = {}

wait_time = 2

def setQ():
    global placement
    global placementDict

    session['id'] = str(uuid4())
    placement += 1
    placementDict[session['id']] = placement
    session['qNumber'] = placementDict[session['id']]

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    serv_time = now + timedelta(minutes=wait_time)
    serve_time = serv_time.strftime("%H:%M:%S")

    session['join'] = current_time
    session['serv'] = serve_time

@app.route('/')
def home():
    setQ()
    num = session['qNumber']
    userId = session['id']
    joinTime = session['join']
    servTime = session['serv']
    return render_template("index.html", num=num, id=userId, tim=joinTime, servTim=servTime)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/queue')
def queue():
    num = session['qNumber']
    userId = session['id']
    joinTime = session['join']
    servTime = session['serv']

    if num is not None or userId is not None or joinTime is not None or servTime is not None:
        return render_template("queue.html", num=num, id=userId, tim=joinTime, servTim=servTime)
    else:
        return render_template("queue.html", num="You have no number", tim="You haven't joined yet", servTim="Never")

@app.route('/leave')
def leave():
    if session['id'] is not None:
        sessID = session['id']
        placementDict.pop(sessID)

        session['id'] = None
        session['qNumber'] = None
        session['join'] = None
        session['serv'] = None

    return render_template("leave.html")

if __name__ == '__main__':
    app.run()
