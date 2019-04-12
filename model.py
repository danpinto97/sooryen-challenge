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
        search_results = []
        title_search = "%" + title + "%"
        c.execute("SELECT * FROM listings WHERE title LIKE ? LIMIT 50",
                  (title_search,))
        results = c.fetchall()
        if len(results) == 0:
            return search_results, datetime.datetime.now(), datetime.datetime.now()
        else:

            for entry in results:
                new_listing = Listing(entry[0], entry[1], entry[2], entry[3])
                search_results.append(new_listing)
            return search_results, results[0][3], results[-1][3]

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
        first_ts= data[0][3]#return first timestamp for accessing previous
        last_ts = data[29][3]#return next timestamp for accessing next
        most_recent_30 = most_recent_30[::-1]
        return most_recent_30, first_ts, last_ts

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
            first_ts = data[0][3]
            new_last_ts = data[-1][3]
        except IndexError:
            more_listings, first_ts, new_last_ts = Listing.get_last_30(c)
        more_listings = more_listings[::-1]
        return more_listings, first_ts, new_last_ts

    @classmethod
    def get_previous_listings(self, c, first_timestamp):
        previous_listings = []
        c.execute("SELECT * FROM listings WHERE ? < time ORDER BY time ASC LIMIT 30 ",
                  (datetime.datetime.strptime(first_timestamp, '%Y-%m-%d %H:%M:%S.%f'),))
        data = c.fetchall()
        for entry in data:
            new_listing = Listing(entry[0], entry[1], entry[2], entry[3])
            previous_listings.append(new_listing)
        try:
            first_ts= data[-1][3]
            last_ts = data[0][3]
        except IndexError:
            previous_listings, first_ts, last_ts = Listing.get_last_30(c)
        return previous_listings, first_ts, last_ts

# testing
if __name__ == '__main__':
    db = 'challenge.db'
    conn = sqlite3.connect(db)
    c = conn.cursor()

    # all_things = Listing.get_all(c)
    # print(len(all_things))
    # for item in all_things:
    #     print(item.print_attributes())
    # first_30, first_ts, last_ts = Listing.get_last_30(c)
    # print('\n', first_ts, last_ts)
    # next_30, first1_ts, last1_ts = Listing.get_more_listings(c, last_ts)
    # print('\n', first1_ts, last1_ts)
    # next_30, first1_ts, last1_ts = Listing.get_more_listings(c, last1_ts)
    # print('\n', first1_ts, last1_ts)
    # prev_30, first2_ts, last2_ts = Listing.get_previous_listings(c, first1_ts)
    # print('\n', first2_ts, last2_ts)
    print(Listing.get_by_title('Ch', c)[0][2].print_attributes())