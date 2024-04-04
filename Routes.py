from flask import Flask, render_template, url_for, redirect, request, session, jsonify, json
from os import path
import sqlite3
from Office import Office

app = Flask(__name__)

app.config['SECRET_KEY'] = "684a2c31fa1f159e791fbd0d01e4214c58b1ba170543bd7085dd61c722617f9f"

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

def get_offices() -> list[Office]:
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT office_name, office_id FROM offices")
    offices = c.fetchall()
    conn.close()

    return [Office(office[0], office[1]) for office in offices]

def get_office(office_id: str) -> Office:
    # Grabs an office by ID.
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    
    try:
        c.execute("SELECT * FROM offices WHERE office_id = $1", (office_id,))
        office = c.fetchone()
        print(office)
        conn.close()
        return Office(name = office[0], id=office[1])
    except sqlite3.OperationalError:
        # Make an error message that will be displayed in place of the office name
        conn.close()
        return Office(name="Cannot find office", id=0)

@app.route("/")
def home():
    return render_template("home.html", title="Home", offices=get_offices()) 

@app.route("/offices/<office_id>")
def office(office_id):
    # Get the office by id from the list of offices
    get_office(office_id)

    office = Office()
    return render_template("building.html", )

intialize_database()


