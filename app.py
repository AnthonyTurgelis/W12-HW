import pandas as pd
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
from bs4 import BeautifulSoup
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from selenium.common.exceptions import ElementNotVisibleException
import json

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Scrape.mars"
mongo = PyMongo(app)


@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


    # render an index.html template and pass it the data you retrieved from the database
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    data = scrape_mars.scrape()
    mars.update({}, data, upsert=True)
    return redirect("/", code=302)

@app.route("/err")
def bad():
    return 1.234

@app.route("/debugged")
def debugged():
    resp = 1.234
    assert isinstance(resp,str), 'response must be string'
    return resp

if __name__ == "__main__":
    app.run(debug=True)
