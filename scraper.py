from bs4 import BeautifulSoup
from requests import get


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

def get_image_urls(listing):
    '''
    Returns the images for a listing. I tried to get this information from the original scrape but was unable to,
    so instead I was able to find it from url link associated with the posting. This takes longer since we need to
    get another link. I am looking into threading to potentially shorten this time.
        Args:
            listing: list obtained by get_all_listings-> 120 indexes of postings to craigslist
        Returns:
            A list of all image urls associated with the listing, if any
    '''
    #need to use the link tot he listing to obtain the pictures, tried doing it all in the orignal page but didn't work
    link = listing.find('a', class_= "result-image gallery").get('href')
    image_soup = BeautifulSoup_it(link)
    return image_soup.find_all('img')


page = BeautifulSoup_it('https://newyork.craigslist.org/search/bka')
for listing in get_all_listings(page):
    print(get_price(listing))
    print(get_title(listing))
    try:
        for image in get_image_urls(listing):
            print(image.get('src'))
    except:
        print("N/a")

    print('\n')