from flask import Flask, render_template, url_for, redirect, request, session, jsonify, json
import os
import random
import sqlite3
from Office import Office

app = Flask(__name__)

app.config['SECRET_KEY'] = "684a2c31fa1f159e791fbd0d01e4214c58b1ba170543bd7085dd61c722617f9f"

def get_offices() -> list[Office]:
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT office_name, office_id FROM offices")
    offices = c.fetchall()
    conn.close()

    return [Office(office[1], office[0]) for office in offices]

@app.route("/",  methods=["GET"])
def home():
    return render_template("home.html", title="Home", offices=get_offices()) 

@app.route("/building/<>",  methods=['GET'])
def anison():
    return render_template("building.html")

# @app.route("/meetingroom/<id>",  methods=['GET', 'POST'])
# def tournament():
#     return render_template("meetingroom.html")

app.run(debug=True)

