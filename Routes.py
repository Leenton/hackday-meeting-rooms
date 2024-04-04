from flask import Flask, render_template, url_for, redirect, request, session, jsonify, json
import qrcode
import qrcode.image.svg
from os import path
import sqlite3
from Issue import Issue
from Office import get_offices, get_office
from Floor import get_floors, get_floor

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



def get_issues_for_meeting_room(resolved:bool, meeting_room_id:int) -> list[Issue]:

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    try:
        c.execute("SELECT issue_note, author_email, created_date, is_resolved, fresh_ticket_id meeting_room_id FROM issues WHERE is_resolved = $1 AND meeting_room_id = $2", (int(resolved) , meeting_room_id))
        issues = c.fetchall()
        conn.close()
        return [Issue(issue[0],issue[1],issue[2],issue[3],issue[4],issue[5]) for issue in issues]
    except sqlite3.OperationalError:
        conn.close()
        return Issue(name="There are no issues", id=0)

@app.route("/")
def home():
    return render_template("home.html", title="Home", offices=get_offices()) 

@app.route("/offices/<office_id>")
def office_page(office_id):
    office = get_office(office_id)
    return render_template("office.html")

@app.route("/meetingroom/<meeting_room_id>")
def meetingroom(meeting_room_id):
    print("WOWOWOWO WEE WA")
    # meetingroom = get_meeting_room(meeting_room_id)


#     return render_template("issues.html", title="Issues", issues=issues)
intialize_database()


