from bs4 import BeautifulSoup
from requests import get
import sqlite3
import datetime

def BeautifulSoup_it(url):
    '''
    This function returns BeautifulSoup of a url passed to it to be scraped
    '''
    site = get(url).text
    return BeautifulSoup(site, 'html.parser')
    #utilize beautifulsoup on the site

def get_all_listings(html_soup):
    '''
    This function returns all 120 postings on the page by finding the li tag with class 'result-row'
        Args:
            html_soup: BeautifulSoup of url we are trying to find listings from ('https://newyork.craigslist.org/search/bka')
        Returns:
            List of all postings from the site
    '''
    return html_soup.find_all('li', class_='result-row')

def get_price(listing):
    '''
    Returns the price of a listing
        Args:
            listing: list obtained by get_all_listings-> 120 indexes of postings to craigslist
        Returns:
            The price of the listing as a string by finding the span tag with class= result-price
    '''
    return listing.find('span', class_="result-price").text

def get_title(listing):
    '''
    Returns the title of a listing
        Args:
            listing: list obtained by get_all_listings-> 120 indexes of postings to craigslist
        Returns:
            The title of the listing as a string by finding the a tag with class= result-image gallery
    '''
    return listing.find('a', class_="result-title hdrlnk").text

def get_image_url(listing):
    '''
    Returns the image for a listing. I tried to get this information from the original scrape but was unable to,
    so instead I was able to find it from url link associated with the posting. This takes longer since we need to
    get another link. I am looking into threading to potentially shorten this time.
        Args:
            listing: list obtained by get_all_listings-> 120 indexes of postings to craigslist
        Returns:
            One image url associated with the listing
    '''

    link = listing.find('a', class_= "result-image gallery").get('href')
    image_soup = BeautifulSoup_it(link)
    return image_soup.find_all('img')[0].get('src')

db = 'challenge.db'
conn = sqlite3.connect(db)
c = conn.cursor()

c.execute("""CREATE TABLE listings(
                    title text,
                    cost text,
                    image_url text,
                    time timestamp,
                    PRIMARY KEY(time)
                    )""")
conn.commit()

page = BeautifulSoup_it('https://newyork.craigslist.org/search/bka')
for listing in get_all_listings(page):
    price = get_price(listing)
    title = get_title(listing)
    try:
        image_url = get_image_url(listing)
        #we check if this has already been added by searching if the url already exists
        c.execute("SELECT * FROM listings WHERE image_url = ?",
                  (image_url,))
        #if not, we add it
        if(len(c.fetchall())==0):
            c.execute("INSERT INTO listings VALUES (?, ?, ?, ?)", (title, price, image_url, datetime.datetime.now()))
    except AttributeError:
        #if there is no available image, check if the name and price already exist
        image_url = ('N/a')
        c.execute("SELECT * FROM listings WHERE title = ? AND cost = ?",
                  (title, price))
        #again- if it doesn't exist we add it
        if (len(c.fetchall()) == 0):
            c.execute("INSERT INTO listings VALUES (?, ?, ?,?)", (title, price, image_url, datetime.datetime.now()))

    conn.commit()

for row in c.fetchall():
    print(row)
conn.commit()
conn.close()