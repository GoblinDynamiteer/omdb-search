# -*- coding: utf-8 -*-
import json
import sys
import re   #regex

# Check if string is an IMDB-id
def is_imdb(string):
    re_imdb = re.compile("^tt\d{1,}")
    return True if re_imdb.search(string) else False

#Check that string is valid type
def valid_type(string):
    re_type = re.compile("(^movie$|^series$|^episode$)")
    return True if re_type.search(string) else False

#Check that string is valid year
def valid_year(string):
    re_year = re.compile("^[1-2]\d{3}$")
    return True if re_year.search(string) else False

site = "http://www.omdbapi.com"

if len(sys.argv) < 3:
    print("Missing arguments: search_query and/or api_key")
    sys.exit()
else:
    api_key = sys.argv[1]
    search_query = sys.argv[2].replace(" ", "+")       #Title or IMDB-id

# Valid types: movie, series, episode
search_year = sys.argv[3] if len(sys.argv) > 3 else "none"
search_type = sys.argv[4] if len(sys.argv) > 4 else "none"

# Build search url
search_string_url = site + "?apikey=" + api_key
if is_imdb(search_query):
    search_string_url += "&i=" + search_query + "&plot=full"
else:
    search_string_url += "&t=" + search_query + "&plot=full"
    if valid_year(search_year):
        search_string_url += "&y=" + search_year
    if valid_type(search_type):
        search_string_url += "&type=" + search_type

print(search_string_url)
