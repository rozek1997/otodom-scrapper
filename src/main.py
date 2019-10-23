import argparse
import json
import math
import os
import time
from urllib.error import HTTPError
from urllib.parse import ParseResult

from scrapping import *

path = os.path.dirname(os.getcwd())  # current working dir
imagePath = path + '/img'  # image path
jsonPath = path + '/json'  # json path
mainURL = ''  # main url with domain name and path variables like: sprzedaz, wynajem
offersQuantity = 0  # variable hold quantity of all offers


#   setup argument parser with 4 arguments
#
def setup():
    parser = argparse.ArgumentParser(description='Provide input')
    parser.add_argument('-p', '--propertytype', nargs='+', required=True,
                        help='Podaj czy interesuje cie dom czy mieszkanie'
                        , type=lambda input: checkArgsCorrectness(parser, ("dom", "mieszkanie"),
                                                                  input))  # lamda invoke checkArgsCorrecteness
    parser.add_argument('-rt', '--rentaltype', nargs='+', required=True,  # to check if passed args are correct
                        help='Podaj czy interesuje cie wynajem czy sprzedaz',
                        type=lambda input: checkArgsCorrectness(parser, ("wynajem", "sprzedaz"), input))
    parser.add_argument('-c', '--city', nargs='+', required=True,
                        help='Podaj misto ktore cie interesuje')
    parser.add_argument('-d', '--district', nargs='+',
                        help='Podaj dzielnice ktore cie interesuje')

    args = parser.parse_args()
    return vars(args)


#   function check if arguments passed from console arr correct
#   parser which is parser instance
#   choices which are list of expected correct value
#   input which is argument value
def checkArgsCorrectness(parser, choices, input):
    if input not in choices:
        parser.error("Args doesn't end with one of {}".format(choices))
    return input


#   function running webscrapper
#   run whole app and download all offers from specific city and district
def getAllOffer():
    s, offersQuantity = getAllPageOffer(mainURL)
    convertToJsonAndSave(s, 1)

    pageQuantity = math.ceil(offersQuantity / offersPerPage)

    # function after downloading first page show statistic about offers
    print("Offers quantity: " + str(offersQuantity))
    print("Offers per page: " + str(offersPerPage))
    print("Pages quantity: " + str(pageQuantity) + "\n\n")
    print("Downloading page: " + str(1) + " " + mainURL)
    print("Page number " + str(1) + " saved")

    if (pageQuantity > 1):
        for i in range(2, pageQuantity + 1):
            # if the HttpError 503 occurs it's mean that otodom.pl prevent from  web scrapping
            # need to wait and download page once again then save
            try:
                pageurl = pageURL(mainURL, i)
                print("Downloading page: " + str(i) + " " + pageurl)
                s, offersQuantity = getAllPageOffer(pageurl)
                convertToJsonAndSave(s, i)
                print("Page number " + str(i) + " saved")
            except HTTPError as httperror:
                if httperror.code == 503:
                    if i > 2:
                        i -= 1
                    else:
                        i = 2
                    time.sleep(0.2)


#   function with 2 args:
#       -array of Apartment object
#       -file name
#   function convert Apartment objects to json and save to file

def convertToJsonAndSave(appartmentArray, fileName):
    with open(jsonPath + '/page' + str(fileName),
              'w') as outfile:
        for appartment in appartmentArray:
            json.dump(appartment.__dict__, outfile, indent=1, separators=(',', ': '))


#  function created url based on category
#   category which was chose with app args
def createURL(rentalType='sprzedaz', propertyType='mieszkanie', city='warszawa', district=''):
    global mainURL
    parsedResult = ParseResult(scheme='https',
                               netloc=hostURL,
                               path=("%s/%s/%s/%s" % (
                                   rentalType.lower(), propertyType.lower(), city.lower(), district.lower())),
                               params='',
                               query=("nrAdsPerPage=%d" % offersPerPage),
                               fragment='')

    mainURL = parsedResult.geturl()


#   function create and setup project dir like /img dir and /dir
def createProjectDirs():
    print("Creating dirs")
    if not os.path.exists(imagePath):
        os.mkdir(imagePath)
    if not os.path.exists(jsonPath):
        os.mkdir(jsonPath)


def main():
    args = setup()
    print("Scrapper was launched")
    try:
        createProjectDirs()  # setup project dirs
        setImagePath(imagePath)  # setup image dir in scrapping.py module
        if not args['district'] is None:  # based on args from input create url with or without district
            createURL(args['rentaltype'][0], args['propertytype'][0], args['city'][0], args['district'][0])
        else:
            createURL(args['rentaltype'][0], args['propertytype'][0], args['city'][0])
        getAllOffer()  # run scraper
    except HTTPError as httperror:  # if http error occur print status of http error
        print("Error occur: " + str(httperror))
    except OSError as oserror:
        print("Creation of the directory failed: " + str(oserror))


if __name__ == "__main__":
    main()
