# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import sys
import os

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# global variable for holding onto all new releases
releases_by_service = {
    "netflix": set([]),
    "hulu": set([]),
    "amazon prime": set([]),
    "hbo": set([])
}

def get_response(url):
    """Makes request to url source and returns response body
    """
    r = requests.get(url)
    return r.text


def scrape_response(resp_body):
    """Scrapes response string and returns BeautifulSoup object
    """
    soup = BeautifulSoup(resp_body, "html.parser")
    return soup


def start_scrape(url):
    """Begins scraping process given a url as input.

    Gets response string from request, makes a scraped response, then parses 
    response looking for specific divs. Adds found links to links_to_visit and
    calls collect_data() on that list of hrefs.
    """
    resp = get_response(url)
    s = scrape_response(resp)

    new_divs = s.findAll("div", {"class": "new"})

    links_to_visit = []

    for div in new_divs:
        links_to_visit.append(div.a["href"])

    collect_data(links_to_visit)


def get_curr_date():
    """"""
    month_num = datetime.now().month #integer from 1-12
    year = datetime.now().year
    return MONTHS[month_num-1], year


def collect_data(links):
    """Takes in a list of links to visit, then recursively calls collect_data() 
    to continue processing of secondary links.

    Function eventually returns None but adds items to global variable with each recursive call.
    """
    if not links:
        return

    lookup_key = links[0][38:41]
    key = None
    for k in releases_by_service:
        if lookup_key in k:
            key = k

    resp = get_response(links[0])
    s = scrape_response(resp)

    p_tags = s.find_all("p", {"class": "clay-paragraph"})

    all_titles = []
    for para in p_tags:
        try:
            # print para.a["href"]
            t = para.find_all("em")
            # titles = [i.replace(u"\u2022", u" ") for i in t]
            # print t
            for em in t:
                # print em.decode('unicode_escape').encode('ascii','ignore')

                if em.string == u' ' or em.string == u'For more coverage of the best movies and TV shows available on ' or em.string == u' and ' or em.string == u'The' or em.string == u'\u2022':
                    continue

                is_bad = False
                for bad in [u'\xa0', u'\u2022 ', u'\u2022\xa0', u'etflix', u'ulu', u'mazon', u'howtime', u'HBO', u'hbo', u'Stream', u'Available', u'month', u',']:
                    if bad in em.string:
                        is_bad = True
                if is_bad:
                    continue

                if u'\u2022\xa0' in em.string:
                    releases_by_service[key].add(em.string.lstrip(u'\u2022\xa0'))
                elif u'\u2022 ' in em.string:
                    releases_by_service[key].add(em.string.lstrip(u'\u2022 '))
                else:
                    releases_by_service[key].add(em.string)
        except:
            continue

    return collect_data(links[1:])


def show_new_releases(service, lookup):
    """Displays titles contained in releases_by_service global dict for pretty 
    rendering in the terminal
    """
    provider = lookup[service-1]

    # print """
    # ======================================================"""
    print """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        {p}
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """.format(p=provider.upper())

    for title in releases_by_service[provider]:
        print "        * {title}".format(title=title.encode('utf8').lstrip()) 

    print """
    ======================================================"""


def show_main_menu(keys):
    """Displays main instructions for CLI tool in legible form
    """
    print """
    ======================================================

    Select a service to view new releases:
    """

    for i, service in enumerate(keys):
        print """
        {item_num}) {service}
        """.format(service=service.upper(), item_num=i+1)

    print """    ======================================================
    """
    print """    <Type "q" to quit>
    """


def show_title_art():
    """Displays main theme art 
    """
    print """
     _______  _______  ______    _______  _______  __   __ 
    |       ||       ||    _ |  |       ||   _   ||  |_|  |
    |  _____||_     _||   | ||  |    ___||  |_|  ||       |
    | |_____   |   |  |   |_||_ |   |___ |       ||       |
    |_____  |  |   |  |    __  ||    ___||       ||       |
     _____| |  |   |  |   |  | ||   |___ |   _   || ||_|| |
    |_______|  |___|  |___|  |_||_______||__| |__||_|   |_|
     _______  _______  ______    _______  _______  _______ 
    |       ||       ||    _ |  |   _   ||       ||       |
    |  _____||       ||   | ||  |  |_|  ||    _  ||    ___|
    | |_____ |       ||   |_||_ |       ||   |_| ||   |___ 
    |_____  ||      _||    __  ||       ||    ___||    ___|
     _____| ||     |_ |   |  | ||   _   ||   |    |   |___ 
    |_______||_______||___|  |_||__| |__||___|    |_______|
    """

    show_banner_art()


def show_banner_art():
    """Displays heading/banner art across CLI tool
    """
    month, year = get_curr_date()
    print """
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        NEW RELEASES
                        {month} {year}
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """.format(month=month, year=year)

def show_exit_art():
    """Displays OH DONKEY meme
    """
    print """

     _______  __   __    ______   _______  __    _  ___   _  _______  __   __ 
    |   _   ||  |_|  |  |  _    ||   _   ||   |_| ||   |_| ||    ___||  |_|  |
    |  | |  ||       |  | | |   ||  | |  ||       ||      _||   |___ |       |
    |  |_|  ||       |  | |_|   ||  |_|  ||  _    ||     |_ |    ___||_     _|
    |_______||__| |__|  |______| |_______||_|  |__||___| |_||_______|  |___|  
    """

    print """
                        ,--._ 
                        `.   `.                      ,-. 
                          `.`. `.                  ,'   ) 
                            \`:  \               ,'    / 
                             \`:  ),.         ,-' ,   / 
                             ( :  |:::.    ,-' ,'   ,' 
                             `.;: |::::  ,' ,:'  ,-' 
                             ,^-. `,--.-/ ,'  _,' 
                            (__        ^ ( _,' 
                          __((o\   __   ,-' 
                        ,',-.     ((o)  / 
                      ,','   `.    `-- ( 
                      |'      ,`        \ 
                      |     ,:' `        | 
                     (  `--      :-.     | 
                     `,.__       ,-,'   ; 
                     (_/  `,__,-' /   ,' 
                     |\`--|_/,' ,' _,' 
                     \_^--^,',-' -'( 
                     (_`--','       `-. 
                      ;;;;'       ::::.`------. 
                        ,::       `::::  `:.   `. 
                       ,:::`       :::::   `::.  \ 
                      ;:::::       `::::     `::  \ 
                      |:::::        `::'      `:   ; 
                      |:::::.        ;'        ;   | 
                      |:::::;                   )  | 
                      |::::::        ,   `::'   |  \ 
                      |::::::.       ;.   :'    ;   ::. 
                      |::::,::        :.  :   ,;:   |:: 
                      ;:::;`"::     ,:::  |,-' `:   |::, 
                      /;::|    `--;""';'  |     :. (`";' 
                      \   ;           ;   |     ::  `, 
                       ;  |           |  ,:;     |  : 
                       |  ;           |  |:;     |  | 
                       |  |           |  |:      |  | 
                       |  |           |  ;:      |  | 
                      /___|          /____|     ,:__| 
                     /    /  -hrr-   /    |     /    ) 
                     `---'          '----'      `---' 
 """


def start_stream_scrape(url):
    """Main function which starts web scraping and maintains rendering of 
    visual components for CLI tool
    """
    os.system('clear')

    new_scrape = start_scrape(url)

    show_title_art()

    dict_keys = releases_by_service.keys()
    show_main_menu(dict_keys)

    while True:
        user_choice = raw_input("    (service) > ")
        os.system('clear')

        if user_choice.lower() == "q":
            show_exit_art()
            print """              %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n                    Thank you for using this tool ^_^\n              Come back next month for more new releases!\n              %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            """
            break
        if user_choice.lower() == "m":
            show_banner_art()
            show_main_menu(dict_keys)
            continue
        try:
            user_choice = int(user_choice)
            if user_choice in range(1,5):
                show_banner_art()
                show_new_releases(user_choice, dict_keys)
                print """
    <HOT TIP: Type "m" for main menu>
    """
            else:
                show_banner_art()
                show_main_menu(dict_keys)
                print "    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n    ¡Please enter a valid choice!\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                continue
        except:
            show_banner_art()
            show_main_menu(dict_keys)
            print "    ~~~~~~~~~~~~~~~~~~~~~~~\n    ¡Please enter a number!\n    ~~~~~~~~~~~~~~~~~~~~~~~\n"


if __name__ == '__main__':
    if len(sys.argv) > 1:
        start_stream_scrape(sys.argv[1])
    else:
        start_stream_scrape("http://www.vulture.com/streaming/")

