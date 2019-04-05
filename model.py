import sqlite3

db = 'challenge.db'
conn = sqlite3.connect(db)
c = conn.cursor()

class Listing(object):
    '''
    Listing class that contains title of the listing, its cost, and the image url.
    '''
    def __init__(self, title, cost, image):
        self.title = title
        self.cost = cost
        self.image = image

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

    def attributes(self):
        return ("Title: %s \nCost: %s \nImage Url: %s" % (self.title, self.cost, self.image))

    @classmethod
    def get_all(self):
        '''
        Returns all listings in database
        '''
        all_listings = []
        c.execute("SELECT * FROM listings")
        for entry in c.fetchall():
            new_listing = Listing(entry[0],entry[1],entry[2])
            all_listings.append(new_listing)
        return all_listings

    @classmethod
    def get_by_title(self, title):
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

#testing
all_things = Listing.get_all()
for item in all_things:
    print(item.attributes())
    print('\n')

print(Listing.get_by_title('Star Wars'))