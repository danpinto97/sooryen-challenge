import sqlite3
import datetime

class Listing(object):
    '''
    Listing class that contains title of the listing, its cost, and the image url.
    '''

    def __init__(self, title, cost, image, timestamp):
        self.title = title
        self.cost = cost
        self.image = image
        self.timestamp = timestamp

    def set_cost(self, cost):
        self.cost = cost

    def set_title(self, title):
        self.title = title

    def set_image(self, image):
        self.image = image

    def get_cost(self):
        return self.cost

    def get_title(self):
        return self.title

    def get_image(self):
        return self.image

    def get_timestamp(self):
        return self.timestamp

    def print_attributes(self):
        return ("Title: %s \nCost: %s \nImage Url: %s \nTimestamp: %s" % (
        self.title, self.cost, self.image, self.timestamp))

    @classmethod
    def get_all(self,c):
        '''
        Returns all listings in database
        '''
        all_listings = []
        c.execute("SELECT * FROM listings ORDER BY time ASC")
        for entry in c.fetchall():
            new_listing = Listing(entry[0], entry[1], entry[2], entry[3])
            all_listings.append(new_listing)
        return all_listings

    @classmethod
    def get_by_title(self, title, c):
        '''
        Returns a listing with a matching title
        '''
        c.execute("SELECT * FROM listings WHERE title LIKE ?",
                  (title,))
        results = c.fetchall()
        if len(results) == 0:
            return 'Not available'
        else:
            return results

    @classmethod
    def get_last_30(self, c):
        '''
        Takes in a cursor. Returns the most recent 30 listings from the database as well as the timestamp of the last from this batch.
        This function is to be used to load the initial listing page with the most recent data and prep for the next
        30 to be loaded.
        '''
        most_recent_30 = []
        c.execute("SELECT * FROM listings ORDER BY time DESC LIMIT 30")
        data = c.fetchall()
        for entry in data:
            new_listing = Listing(entry[0], entry[1], entry[2], entry[3])
            most_recent_30.append(new_listing)
        last_ts = data[29][3]
        return most_recent_30, last_ts

    @classmethod
    def get_more_listings(self, c, last_timestamp):
        '''
        Takes in a cursor and the last timestamp. Finds the next 30 listings based on a previous timestamp and returns
        them plus the last timestamp of these values to be used to find the next batch.
        '''
        more_listings = []
        c.execute("SELECT * FROM listings WHERE ? > time ORDER BY time DESC LIMIT 30 ",
                  (datetime.datetime.strptime(last_timestamp, '%Y-%m-%d %H:%M:%S.%f'),))
        data = c.fetchall()
        for entry in data:
            new_listing = Listing(entry[0], entry[1], entry[2], entry[3])
            more_listings.append(new_listing)
        try:
            new_last_ts = data[-1][3]
        except:#have to fix with correct error, but basically returns 0 if there is no more data
            new_last_ts = 0
            print(data)
        return more_listings, new_last_ts


# testing
if __name__ == '__main__':
    db = 'challenge.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()

    all_things = Listing.get_all(c)
    print(len(all_things))
    for item in all_things:
        print(item.print_attributes())
