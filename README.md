#Install package

    In folder /src:
    pip3 install -r requirements.txt

#Run scrapper

    python3 main.py with arguments
    
    Arguments:

    For help:
    -h, --help            show this help message and exit

    Essential arguments:
  
    -p                     Podaj czy interesuje cie dom czy mieszkanie
    -rt                    Podaj czy interesuje cie wynajem czy sprzedaz
    -c                     Podaj misto ktore cie interesuje
    
    Optional arguments:
    
    -d                     Podaj dzielnice ktore cie interesuje
    
    Example: 
    
    python3 main.py -p mieszkanie -rt wynajem -c warszawa -d bemowo


#Additional info
    Scrapper create dirs /img & /json collaterally to /src dir
    In /img dir scrapper saves all photos
    In /json dir scrapper saves info from Query in JSON format
    
#How it works
    Scraper downloads all pages from category based on user args input
    
    If scrapper will not find any page the error will be thrown
    
    Scraper goes throught all pages in specific category en route and gets single
    offer then gets inside to subpage of that offer and mine additional information
    Then it goes to the next offers.
    Page by page
    
    Scraper can run into problem when otodom.pl will block the queries for pages.
    If than problem occurs scrapper waits 200 ms then it tries again.
    
    Json files for each page are saved in current working dircetory in subdir ./json
    Image are saved in current working directory in subdir ./img
