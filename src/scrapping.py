import re
from urllib.parse import urlparse
from urllib.request import Request
from urllib.request import urlopen
from urllib.request import urlretrieve

from bs4 import BeautifulSoup as bs

hostURL = 'www.otodom.pl'  # domain name for which
imagePath = ''  # path where image will be stored, generated after application started
offersPerPage = 24  # hardcoded quantity offers per page
regex = re.compile("^.*}+", re.IGNORECASE)


#   class used for creating Apartment object which later
#   is used for conversion to JSON and saving to file
class Apartment:

    def __init__(self, name, location, price, image, overview=[]):
        self.name = name
        self.location = location
        self.price = price
        self.image = image
        self.overview = overview


#   function build new url address
#   created for searching through pages page by page
def pageURL(mainURL, pageNumber):
    queryURL = ("%s&page=%d" % (mainURL, pageNumber))
    return queryURL


#   function getting url for only one element (offer) on page
#   it is getting inside to subpage and scraping all detailed info about this offer
#       name
#       location
#       price
#       image which save only to Apartment object name of image, and download image to /img directory
#       details from section-overview
#
#       return new Apartment object with all above details
#
def getDetailedInfo(url):
    htmlPage = downloadPage(url)

    headerContainer = htmlPage.find('header')  # find header container which contain info like name, price, loc

    pictureContainer = htmlPage.find('picture')  # find picture container
    overviewContainer = htmlPage.find('section', class_='section-overview')  # find overview container



    return Apartment(name=headerContainer.find('h1').text,
                     location=re.sub(regex, ' ', headerContainer.find('div', class_='css-0').find('a').get_text()),
                     price=headerContainer.find('div', class_='css-1vr19r7').text,
                     image=downloadImage(pictureContainer.find('img').get('src')),
                     overview=getOverviewFromPost(overviewContainer))


#   download new page and parse with html5lib  based on url argument
#   return parsed html file
#   can throw HttpError like 404 -Not found or 503
def downloadPage(url):
    req = Request(url, headers={
        'User-Agent': "Mozilla/5.0"})  # need to use this header to trick otodom.pl that "Key, i'm web browser Moziilla"
    sauce = urlopen(req).read()  # otherwise otodom.pl is safe against web scraping

    soup = bs(sauce, 'html5lib')
    return soup


#   function getting detail from subpage of single offer
#   from container class=section-overview
#   return list of details
#   every offer has diffrent list of details
def getOverviewFromPost(sectionOverview):
    overViewList = []
    for litag in sectionOverview.find_all('li'):
        overViewList.append(litag.text)

    return overViewList


#   function downloading image and getting its name from url address
def downloadImage(url):
    urlretrieve(url, imagePath + "/" + urlparse(url).path.split('/')[-2])

    return urlparse(url).path.split('/')[-2]


# download all offers from page based on args
#       -url
#   return array of all post on page and sum of offers in specific category
def getAllPageOffer(url):
    htmlPage = downloadPage(url)

    divContainer = htmlPage.find('div', class_='listing')
    offersQuantity = int(htmlPage.find('div', class_='offers-index').find('strong').text)  # convert text to string

    allPost = []
    for articleTag in divContainer.find_all('article', class_='offer-item'):
        allPost.append(getDetailedInfo(articleTag.get('data-url')))

    return allPost, offersQuantity


#   used for setting global value imagePath
def setImagePath(path):
    global imagePath
    imagePath = path
