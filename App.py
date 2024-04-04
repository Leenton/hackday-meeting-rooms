from flask import Flask, request, jsonify, render_template, url_for 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('buildings.html')

@app.route('/buildings/<buildingName>')
def buildings():
    return render_template('building.html')