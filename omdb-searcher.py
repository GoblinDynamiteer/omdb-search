# -*- coding: utf-8 -*-
import json, urllib.request, sys, re

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

class Movie:
    def __init__(self, json_data):
        self.title = json_data["Title"]
        self.year = json_data["Year"]
        self.imdb_id = json_data["imdbID"]
        self.imdb_rating = json_data["Ratings"][0]["Value"]
        self.genre = json_data["Genre"]
        self.actors = json_data["Actors"]
        self.runtime = json_data["Runtime"]
    def to_string(self):
        print(self.title + " (" + self.year +")")
        print(self.imdb_id)
        print(self.genre)
        print("Runtime: " + self.runtime)
        print("IMDb rating: " + self.imdb_rating)
        print("Actors: " + self.actors)

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
try:
    response = urllib.request.urlopen(search_string_url).read().decode("utf-8")
    json_data = json.loads(response)
    data = Movie(json_data)
    data.to_string()

except:
    print("Error searching for " + search_query)
    pass
