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
        self.country = json_data["Country"]
    def to_string(self):
        print("Movie: " + self.title + " (" + self.year +")")
        print(self.country)
        print(self.imdb_id)
        print(self.genre)
        print("Runtime: " + self.runtime)
        print("IMDb rating: " + self.imdb_rating)
        print("Actors: " + self.actors)

class Show:
    def __init__(self, json_data):
        self.title = json_data["Title"]
        self.year = re.sub('[^\x00-\x7f]','-', json_data["Year"])
        self.imdb_id = json_data["imdbID"]
        self.imdb_rating = json_data["Ratings"][0]["Value"]
        self.genre = json_data["Genre"]
        self.actors = json_data["Actors"]
        self.runtime = json_data["Runtime"]
        self.season_count = json_data["totalSeasons"]
        self.episode_count = 0
        self.country = json_data["Country"]
        self.seasons = None

        self.__find_episodes()

    def to_string(self):
        print("Show: " + self.title + " (" + self.year +")")
        print(self.country)
        print(self.season_count + " seasons")
        print(self.imdb_id)
        print(self.genre)
        print("Runtime: " + self.runtime)
        print("IMDb rating: " + self.imdb_rating)
        print("Actors: " + self.actors)

    def list_episodes(self):
        if self.seasons == None:
            self.__find_episodes()
        for season in self.seasons:
            for episode in season.episodes:
                episode.to_string()

    def __find_episodes(self):
        self.seasons = []
        for i in range(0, int(self.season_count)):
            url = site + "?apikey=" + api_key + "&i=" + self.imdb_id + \
                "&season=" + str(i+1)
            try:
                response = urllib.request.urlopen(url).read().decode("utf-8")
                json_data = json.loads(response)
                self.seasons.append(Season(json_data, i+1))
                self.episode_count += self.seasons[i].episode_count
            except:
                pass


class Season:
    def __init__(self, json_data, season_number):
        self.episode_count = len(json_data["Episodes"])
        self.season_number = season_number
        self.episodes = []
        for i in range(0, int(self.episode_count)):
            title = json_data["Episodes"][i]["Title"]
            date = json_data["Episodes"][i]["Released"]
            self.episodes.append(Episode(title, i+1, self.season_number, date))

class Episode:
    def __init__(self, title, number, season_number, release_date):
        self.number = number
        self.title = title
        self.season_number = season_number
        self.release_date = release_date
    def to_string(self):
        print("S" + "%02d" % self.season_number + "E" + \
            "%02d" % self.number + ": " + self.title + \
            " (" + self.release_date + ")")


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

except:
    print("Error searching for " + search_query)
    sys.exit()

if json_data["Type"] == "series":
    data = Show(json_data)

if json_data["Type"] == "movie":
    data = Movie(json_data)

data.to_string()
if hasattr(data, 'list_episodes') and False:
    print("\nEpisodes (" + str(data.episode_count) + ")")
    data.list_episodes()
