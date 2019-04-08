from flask import Flask, render_template, request
from model import Listing
import sqlite3
db = 'challenge.db'
conn = sqlite3.connect(db)
c = conn.cursor()

app = Flask(__name__)


@app.route('/')
def index():
    #load the homepage
    return render_template('home.html')

@app.route('/about')
def about():
    #load the about page
    return render_template('about.html')

@app.route('/listings', methods=['GET','POST'])
def listings():
    #load the listing page
    with sqlite3.connect('challenge.db') as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            #check for post method and set last timestamp returned from html request
            last_timestamp = list(request.form.to_dict())[0]

            #use get_more_lastings with last timestamp to obtain next 30 listings
            listings, last_timestamp = Listing.get_more_listings(cursor, last_timestamp)
            return render_template('listings.html', listings = listings, last_timestamp= last_timestamp)
        else:
            #if there is no post, we load the page with the most recent listings
            listings, last_timestamp= Listing.get_last_30(cursor)
            return render_template('listings.html', listings = listings, last_timestamp= last_timestamp)


if __name__ == '__main__':
    app.run()