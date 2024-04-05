from flask import Flask, render_template, url_for, redirect, request, make_response
from qrcode import make
from qrcode.image.svg import SvgImage
from os import path
import sqlite3
from Office import get_offices, get_office
from Floor import get_floor
from MeetingRoom import get_meeting_room
from Issue import Issue, create_ticket, VALID_EMAIL
from secrets import token_hex
import re
from html import escape
from datetime import datetime


app = Flask(__name__)

app.config['SECRET_KEY'] = token_hex(32) 
DOMAIN_NAME = "localhost:5000"

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

def render_meeting_room_page(meeting_room_id: int, errors: list[str] = []):
    try:
        meeting_room = get_meeting_room(meeting_room_id)
        floor = get_floor(meeting_room.floor_id)
        office = get_office(floor.office_id)
        issues = meeting_room.get_issues(False)

        return render_template("meetingroom.html", meeting_room=meeting_room, floor=floor, office=office, issues=issues, errors=errors)
    except:
        return redirect(url_for("error_page"))

@app.route("/meetingroom/<meeting_room_id>", methods=["GET", "POST"])
def meeting_room_page(meeting_room_id):
    if request.method == "GET":
        return render_meeting_room_page(meeting_room_id, errors = [])
    elif request.method == "POST":
        email = request.form.get("email", '')
        note = request.form.get("note")

        if not re.match(VALID_EMAIL, email):
            return render_meeting_room_page(meeting_room_id, errors=["Invalid email address."])
        if not note:
            return render_meeting_room_page(meeting_room_id, errors=["Note cannot be empty."])
        
        meeting_room = get_meeting_room(meeting_room_id)
        floor = get_floor(meeting_room.floor_id)
        office = get_office(floor.office_id)
        full_meeting_room_name = f"{office.name} - Floor: {floor.floor_num} - {meeting_room.name}"
        ticket_id = create_ticket(email, note, full_meeting_room_name)

        if not ticket_id:
            return render_meeting_room_page(meeting_room_id, errors=["Issue could not be created. Please try again or contact the administrator for help if it keeps happening."])
        
        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        try:
            c.execute(
                "INSERT INTO issues (author_email, created_date, fresh_ticket_id, is_resolved, issue_note, meeting_room_id) VALUES (?, ?, ?, ?, ?, ?)",
                (email, int(datetime.now().timestamp()), ticket_id, 0, escape(note), meeting_room.id)
            )
            conn.commit()
            conn.close()

            return render_meeting_room_page(meeting_room_id, errors = [])
        except:
            return redirect(url_for("error_page"))
    else:
        return redirect(url_for("error_page"))
    
@app.route("/issues/<meeting_room_id>")
def issue_page(meeting_room_id):
    try:
        resolved = int(request.args.get("resolved", 3))
        if resolved == 3:
            raise Exception("resolved is a required parameter.")
    
        return render_template("issues.html", issues=get_meeting_room(meeting_room_id).get_issues(bool(resolved)))
    except:
        return "Something went wrong. Contact the administrator or try again."

@app.route("/qr/<meeting_room_id>")
def qr_code_page(meeting_room_id):
    response = make_response(
        make(
            (DOMAIN_NAME + '/meetingroom/' + meeting_room_id ),
            box_size=50,
            image_factory=SvgImage
        ).to_string()
    )
    response.headers['Content-Type'] = 'image/svg+xml'
    return response

@app.route("/error")
def error_page():
    return render_template("error.html")
    

intialize_database()

app.run(debug=True)
