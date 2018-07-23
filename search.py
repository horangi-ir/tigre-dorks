import datetime
import json
import boto3
import argparse

from engines import duckduckgo, bing, dogpile
from time import sleep

words = [
    {
        "string": '"# Position (offset in bytes) in this file for beginning of each section for"',
        "identifier": [("summary", "AWSTATS DATA FILE")],
        "group": "awstats-data-file",
        "verify": False
    },
    {
        "string": '"Contributors: the WordPress team"',
        "identifier": [("file", "readme.txt")],
        "group": "wordpress-contributors",
        "verify": True
    },
    {
        "string": '"Tags: Jetpack, WordPress.com, backup, security, related posts, CDN, speed, anti-spam, social sharing, SEO, video, stats"',
        "identifier": [("file", "readme.txt")],
        "group": "wordpress-tags",
        "verify": True
    },
    {
        "string": '"Welcome to PHP-Nuke" congratulations',
        "identifier": [("summary", "Welcome to PHP-Nuke! Congratulations! You have now a web portal installed!. You can edit")],
        "group": "postnuke",
        "verify": False
    }
]

parser = argparse.ArgumentParser(description='Search...')
parser.add_argument("-f", "--filename",
                    nargs=1, help="Filename")
parser.add_argument("-nu", "--noupload",
                    action="store_true", help="Don't upload")
args = parser.parse_args()


def save(engine, obj, group):
    print("Saving to file...")
    timestamp = args.filename[0] if args.filename \
        else datetime.datetime.now().isoformat()
    dataFile = ".".join([group, engine, timestamp, "json"])
    with open(dataFile, "w+") as f:
        json.dump(obj, f, indent=2)
    # TODO: Read access and secret from file or env!
    if not args.noupload:   # No upload option
        print("Uploading file to DO Space...")
        session = boto3.session.Session()
        client = session.client(
                's3',
                region_name='nyc3',
                endpoint_url='https://nyc3.digitaloceanspaces.com',
                aws_access_key_id='',
                aws_secret_access_key=''
            )

        client.upload_file(dataFile,  # Path to local file
                           'osint-collection',  # Name of Space
                           dataFile)  # Name for remote file
        print("Uploading complete [%s]" % dataFile)


def search():
    for w in words:
        ret = duckduckgo.search(w['string'], w['identifier'])
        if ret:
            save("duckduckgo", ret, w['group'])
        ret = bing.search(w['string'], w['identifier'])
        if ret:
            save("bing", ret, w['group'])
        ret = dogpile.search(w['string'], w['identifier'])
        if ret:
            save("dogpile", ret, w['group'])
        print("I'll sleep for a while...")
        sleep(120)  # Don't spam the search engines!
        print("Continuing search...")
    print("Done!")


if __name__ == "__main__":
    search()
