import requests
import json

from . import headers, is_match, get_unique
from urllib.parse import unquote
from bs4 import BeautifulSoup as BS


url = "https://duckduckgo.com/html/"


def next_page(soup):
    form = soup.find("div", class_="nav-link")
    fields = form.find_all("input")
    params = {}
    for field in fields:
        if "name" in field.attrs.keys():
            params[field['name']] = field['value']
    res = requests.post(url, params=params, headers=headers)
    if res.status_code == 200:
        soup = BS(res.text, 'html.parser')
        return soup


def parse(soup, _filter=None):
    res = soup.find_all("a", class_="result__snippet")
    obj = []
    for x in res:
        text = x.text
        url = unquote(x['href'].split("uddg=")[1]) \
            if "uddg=" in x['href'] else x['href']
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
    html = requests.get(url, params={"q": query}, headers=headers)
    if html.status_code == 200:
        soup = BS(html.text, 'html.parser')
        obj = []
        while soup:
            print("Querying DuckDuckGo...")
            res = get_unique(obj, parse(soup, _filter))
            print("Found %i results" % len(res))
            obj.extend(res)
            soup = next_page(soup)
        print("Found a total of %i results" % len(obj))
        return obj
    print(html.status_code, html.text)
