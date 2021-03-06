from flask import Flask, render_template, jsonify, redirect, request
from pymongo import MongoClient
from flask_pymongo import PyMongo
import pandas as pd
import csv
import os

#from ipynbfiledconverted import the function

app = Flask(__name__)

# from pymongo import MongoClient

# client = MongoClient(os.environ['MONGOLAB_URI'])
# db = client.get_default_database()

mongolab_uri = os.getenv('MONGOLAB_URI')

if mongolab_uri:
    app.config["MONGO_URI"] = mongolab_uri
else:
    app.config["MONGO_URI"] = "mongodb://localhost:27017/planets_db"
mongo = PyMongo(app)
mongo.db.planets_db.drop()
info = pd.read_csv("datasets/cleaned_planets.csv", index_col=False).drop("Unnamed: 0", axis=1)
info_json = info.to_dict(orient='records')
mongo.db.planets_db.insert_many(info_json)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/bubble")
def bubble():
    return render_template("bubble_chart.html")

@app.route("/distance")
def distance():
    return render_template("distance_earth.html")

@app.route("/data")
def data():
    planet_data = list(mongo.db.planets_db.find({}, {"_id": 0 }))
    return jsonify(planet_data)


if __name__ == "__main__":
    app.run(debug=True, port=9000)