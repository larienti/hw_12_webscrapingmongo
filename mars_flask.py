
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
#I'm not sure if this is the correct socket or as they call it "pipline"
#can't find image_urls... not sure why 


@app.route("/")
def home():
    data = mongo.db.collection.find_one()
    #find our database...... is the problem here? 
    return render_template("index.html", mars=data)


@app.route("/scrape")
def scrape():
    data = scrape_mars.scrape()
    # upsert into collection
    mongo.db.collection.update({}, data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)