from flask import Flask, render_template, url_for, redirect, request, session, jsonify, json
import qrcode
import qrcode.image.svg
from os import path
import sqlite3
from Issue import Issue
from Office import get_offices, get_office
from Floor import get_floors, get_floor
from MeetingRoom import MeetingRoom, get_meeting_room

app = Flask(__name__)

app.config['SECRET_KEY'] = "684a2c31fa1f159e791fbd0d01e4214c58b1ba170543bd7085dd61c722617f9f"

DOMAIN_NAME = "localhost:5000"

def generate_qr_code(path: str) -> str:
    img = qrcode.make((DOMAIN_NAME + path), image_factory=qrcode.image.svg.SvgImage)
    return img.to_string()

def intialize_database() -> None:
    if not path.exists("data.db"):
        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        #get the contents of the schema file
        with open("schema.sql") as f:
            schema = f.read()
        
        c.executescript(schema)
        c.close()
        conn.commit()

        #add the sample data in data.sql to the database
        c = conn.cursor()

        with open("data.sql") as f:
            data = f.read()

        c.executescript(data)
        conn.commit()
        c.close()
        conn.close()

@app.route("/")
def home_page():
    try:
        return render_template("home.html", title="Home", offices=get_offices()) 
    except:
        return redirect(url_for("error_page"))

@app.route('/offices/<office_id>')
def office_page(office_id):
    try:
        return render_template("office.html", office=get_office(office_id))
    except:
        return redirect(url_for("error_page"))

@app.route("/meetingroom/<meeting_room_id>")
def meeting_room_page(meeting_room_id):
    try:
        return render_template("meetingroom.html", meeting_room=get_meeting_room(meeting_room_id))
    except:
        return redirect(url_for("error_page"))
    
@app.route("/issues/<issue_id>")
def issue_page(issue_id):
    try:
        return render_template("issue.html", issue=Issue(issue_id))
    except:
        return redirect(url_for("error_page"))


@app.route("/error")
def error_page():
    print("")
    return render_template("error.html")
    



# intialize_database()

app.run(debug=True)
