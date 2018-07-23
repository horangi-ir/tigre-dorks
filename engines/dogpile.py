import requests
import json

from . import headers, is_match, get_unique
from urllib.parse import unquote
from bs4 import BeautifulSoup as BS
from time import sleep


url = "https://www.dogpile.com/info.dogpl/search/web"


def next_page(soup):
    next_link = soup.find("li", class_="paginationNext")
    if not next_link:
        return
    params = next_link.a['href'][22:]

    sleep(3)  # Slowdown to not get blocked
    res = requests.get("".join([url, params]), headers=headers, verify=False)
    if res.status_code == 200:
        soup = BS(res.text, 'html.parser')
        return soup


def parse(soup, _filter=None):
    res = soup.find_all("div", class_="searchResult webResult")
    obj = []
    for x in res:
        text = x.find("div", class_="resultDescription").text
        url = unquote(unquote(
                    x.find("a", class_="resultDisplayUrl")['href']
                    .split("%26ru%3d")[1]
                    .split("%26du%3d")[0]
                ))
        if not is_match(_filter, text, url):
            continue
        obj.append(
            {
                "val": text,
                "url": url
            }
        )
    return obj


def search(query, _filter=None):
    params = {
        "fcoid": 417,
        "fcop": "topnav",
        "fpid": 27,
        "om_nextpage": True,
        "q": query,
        "ql": None
    }
    # TODO: dogpile has problems with HTTPS verification when running from code
    # Is verify=False enough for security?
    html = requests.get(url, params=params, headers=headers, verify=False)
    if html.status_code == 200:
        soup = BS(html.text, 'html.parser')
        obj = []
        while soup:
            print("Querying dogpile...")
            res = get_unique(obj, parse(soup, _filter))
            print("Found %i results" % len(res))
            obj.extend(res)
            soup = next_page(soup)
        print("Found a total of %i results" % len(obj))
        return obj
    print(html.status_code, html.text)
