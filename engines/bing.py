import requests
import json

from . import headers, is_match, get_unique
from urllib.parse import unquote
from bs4 import BeautifulSoup as BS


url = "https://www.bing.com/search"


def next_page(soup):
    next_link = soup.find("a", class_="sb_pagN ")
    if not next_link:
        return
    params = next_link['href'][7:]
    res = requests.get("".join([url, params]), headers=headers)
    if res.status_code == 200:
        soup = BS(res.text, 'html.parser')
        return soup


def parse(soup, _filter=None):
    res = soup.find_all("li", class_="b_algo")
    obj = []
    for x in res:
        text = x.find("div", class_="b_caption").p.text
        url = x.h2.a['href']
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
        "q": query,
        "go": "Search"
    }
    html = requests.get(url, params=params, headers=headers)
    if html.status_code == 200:
        soup = BS(html.text, 'html.parser')
        obj = []
        while soup:
            print("Querying Bing...")
            res = get_unique(obj, parse(soup, _filter))
            print("Found %i results" % len(res))
            obj.extend(res)
            soup = next_page(soup)
        print("Found a total of %i results" % len(obj))
        return obj
    print(html.status_code, html.text)
