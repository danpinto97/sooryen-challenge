from flask import Flask, render_template, request
from model import Listing
import sqlite3
db = 'challenge.db'
conn = sqlite3.connect(db)
c = conn.cursor()

application = app = Flask(__name__)


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
            request_dict = request.form.to_dict()
            for k,v in request_dict.items():
                timestamp_to_be_used = k
                if v == 'Load more posts':
                    #use get_more_lastings with last timestamp to obtain next 30 listings
                    listings, first_timestamp, last_timestamp = Listing.get_more_listings(cursor, timestamp_to_be_used)
                else:
                    listings, first_timestamp, last_timestamp = Listing.get_previous_listings(cursor, timestamp_to_be_used)
                return render_template('listings.html', listings = listings, first_timestamp = first_timestamp, last_timestamp= last_timestamp)
        else:
            #if there is no post, we load the page with the most recent listings
            listings, first_timestamp, last_timestamp = Listing.get_last_30(cursor)
            return render_template('listings.html', listings = listings, first_timestamp = first_timestamp,last_timestamp= last_timestamp)

@app.route('/search', methods=['GET'])
def search():
    with sqlite3.connect('challenge.db') as conn:
        cursor = conn.cursor()
        return render_template('search.html')

if __name__ == '__main__':
    app.run()