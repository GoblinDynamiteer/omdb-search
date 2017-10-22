# -*- coding: utf-8 -*-
import json, urllib.request, sys, re, argparse

# Check if string is an IMDB-id
def is_imdb(string):
    re_imdb = re.compile("^tt\d{1,}")
    return True if re_imdb.search(string) else False

#Check that string is valid type
def valid_type(string):
    if string == None:
        return False
    re_type = re.compile("(^movie$|^series$|^episode$)")
    return True if re_type.search(string) else False

#Check that string is valid year
def valid_year(string):
    if string == None:
        return False
    re_year = re.compile("^[1-2]\d{3}$")
    return True if (re_year.search(string) or string != None) else False

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
            url = site + "?apikey=" + args.api_key + "&i=" + self.imdb_id + \
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

parser = argparse.ArgumentParser(description='OMDb search')
parser.add_argument('-api', dest='api_key', type=str, help='API key (Required)')
parser.add_argument('query', type=str, help='Search query')
parser.add_argument('-year', dest='search_year', help='Year')
parser.add_argument('-type', dest='search_type', help='Type: movie, series, episode')
parser.add_argument('-output', dest='output', \
    help='Output: full, imdb, title, year, genre, episode_list, episode_count') # -o works
args = parser.parse_args()

# Build search url
search_string_url = site + "?apikey=" + args.api_key
if is_imdb(args.query):
    search_string_url += "&i=" + args.query + "&plot=full"
else:
    search_string_url += "&t=" + re.sub('\s+', '+', args.query) + "&plot=full"
    if valid_year(args.search_year):
        search_string_url += "&y=" + args.search_year
    if valid_type(args.search_type):
        search_string_url += "&type=" + args.search_type
try:
    response = urllib.request.urlopen(search_string_url).read().decode("utf-8")
    json_data = json.loads(response)
    if json_data["Type"] == "series":
        data = Show(json_data)

    if json_data["Type"] == "movie":
        data = Movie(json_data)

except:
    print("Error searching for " + args.query)
    print("String Generated: " + search_string_url)
    sys.exit()

# Output
if args.output == "full":
    data.to_string()
    if hasattr(data, 'list_episodes'):
        print("\nEpisodes (" + str(data.episode_count) + ")")
        data.list_episodes()
elif args.output == "episode_list":
    if hasattr(data, 'list_episodes'):
        data.list_episodes()
    else:
        print("No episodes available for " + data.title)
elif args.output == "episode_count":
    if hasattr(data, 'episode_count'):
        print(data.episode_count)
    else:
        print("No episodes available for " + data.title)
elif args.output == "imdb":
    print(data.imdb_id)
elif args.output == "title":
    print(data.title)
elif args.output == "genre":
    print(data.genre)
elif args.output == "year":
    print(data.year)
else: # No output argument given
    data.to_string()
