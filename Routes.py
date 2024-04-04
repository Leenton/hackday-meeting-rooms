from flask import Flask, render_template, url_for, redirect, request, session, jsonify, json
import os
import random
import sqlite3
from Office import Office

app = Flask(__name__)

app.config['SECRET_KEY'] = "684a2c31fa1f159e791fbd0d01e4214c58b1ba170543bd7085dd61c722617f9f"


#Check if data.db exists, if not create it
if not os.path.exists("data.db"):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    #get the contents of the schema file
    with open("schema.sql") as f:
        schema = f.read()
    
    c.executescript(schema)
    conn.commit()
    conn.close()



def get_offices() -> list[Office]:
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT office_name, office_id FROM offices")
    offices = c.fetchall()
    conn.close()

    return [Office(office[0], office[1]) for office in offices]

@app.route("/",  methods=["GET"])
def home():
    return render_template("home.html", title="Home", offices=get_offices()) 

@app.route("/building/<>",  methods=['GET'])
def anison():
    return render_template("building.html")

app.run(debug=True)

