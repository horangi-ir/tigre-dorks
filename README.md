# osint_log_search
Originally, the script was developed to search for logs leaked by search
engines such as Bing, DuckDuckGo and Dogpile using Google Dorks. However,
Google Dork also offers searches to find other server problems such as:
1. Leaked credentials
2. Leaked configuration files
3. Outdated services
4. Vulnerable services


## How to use
`python search.py -f <filename> -nu`

Currently the script is implemented to upload the files to DO by default.
The `-nu` is necessary to disable the upload functionality.

The output filename can be indicated via `-f`


## TODO
* Add more search engines
* Add more google dorks [https://www.exploit-db.com/google-hacking-database/]