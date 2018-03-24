# -*- coding: utf-8 -*-
import json, urllib, sys, re, os

site = "http://www.omdbapi.com"

class omdb_search:
    def __init__(self, search_string, search_type, search_year, api_key = None):
        _apk = self._load_api_key()
        self.url_args = {}
        if not _apk and api_key:
            print("Using passed API-key")
            _apk = api_key
        elif not _apk:
            print("no valid API-key found or passed, quitting")
            quit();
        self.url_args['apikey'] = _apk
        self.json_data = ""
        if self._is_imdb(search_string):
            self.url_args['i'] = search_string
        else:
            self.url_args['t'] = search_string
            if self._valid_year(search_year):
                self.url_args['y'] = search_year
            if self._valid_type(search_type):
                self.url_args['type'] = search_type
        self.url_args['plot'] = "full"
        self.search_string_url = site + "?" + urllib.parse.urlencode(self.url_args)
        self._search();

    def get_url(self):
        return self.search_string_url

    def get_api(self):
        return self.url_args['apikey']

    def _search(self):
        try:
            response = urllib.request.urlopen(self.search_string_url, timeout = 4) \
                .read().decode("utf-8")
            self.json_data = json.loads(response)
        except:
            self.json_data = None

    # Load API-key from text-file in same directory as script file
    def _load_api_key(self):
        script_path = os.path.dirname(os.path.realpath(__file__))
        api_txt = os.path.join(script_path, "omdb_api.txt")
        try:
            f = open(api_txt, "r")
            key = f.readline().strip('\n')
            f.close()
            return key
        except:
            print("Could not load OMDb API-key from file")
            return None

    def data(self):
        return self.json_data

    def get_type(self):
        try:
            if self.json_data["Type"] == "series":
                return "series"
            if self.json_data["Type"] == "movie":
                return "movie"
            else:
                return None
        except:
            return None

    # Check if string is an IMDB-id
    def _is_imdb(self, string):
        re_imdb = re.compile("^tt\d{1,}")
        return True if re_imdb.search(string) else False

    #Check that string is valid type
    def _valid_type(self, string):
        if string == None:
            return False
        re_type = re.compile("(^movie$|^series$|^episode$)")
        return True if re_type.search(string) else False

    #Check that string is valid year
    def _valid_year(self, string):
        if string == None:
            return False
        re_year = re.compile("^[1-2]\d{3}$")
        return True if (re_year.search(string) or string != None) else False

class omdb_movie_data:
    def __init__(self, omdb):
        self.omdb = omdb
        self.json = self.omdb.data()
        self.title = self.json["Title"]
        self.year = self.json["Year"]
        self.imdb_id = self.json["imdbID"]
        try:
            self.imdb_rating = self.json["Ratings"][0]["Value"]
        except:
            self.imdb_rating = "N/A"
        self.genre = self.json["Genre"]
        self.actors = self.json["Actors"]
        self.runtime = self.json["Runtime"]
        self.country = self.json["Country"]
    def to_string(self):
        print("omdb_movie_data: " + self.title + " (" + self.year +")")
        print(self.country)
        print(self.imdb_id)
        print(self.genre)
        print("Runtime: " + self.runtime)
        print("IMDb rating: " + self.imdb_rating)
        print("Actors: " + self.actors)

class omdb_tv_data:
    def __init__(self, omdb):
        self.omdb = omdb
        self.json = self.omdb.data()
        self.title = self.json["Title"]
        self.year = re.sub('[^\x00-\x7f]','-', self.json["Year"])
        self.imdb_id = self.json["imdbID"]
        self.imdb_rating = self.json["Ratings"][0]["Value"]
        self.genre = self.json["Genre"]
        self.actors = self.json["Actors"]
        self.runtime = self.json["Runtime"]
        self.season_count = self.json["totalSeasons"]
        self.episode_count = None
        self.country = self.json["Country"]
        self.seasons = None

        #self.__find_episodes()

    def to_string(self):
        print("omdb_tv_data: " + self.title + " (" + self.year +")")
        print(self.country)
        print(self.season_count + " seasons")
        print(self.imdb_id)
        print(self.genre)
        print("Runtime: " + self.runtime)
        print("IMDb rating: " + self.imdb_rating)
        print("Actors: " + self.actors)

    def list_episodes(self):
        if self.seasons is None:
            self.__find_episodes()
        for season in self.seasons:
            for episode in season.episodes:
                episode.to_string()

    def get_episode_count(self):
        if self.episode_count is None:
            self.__find_episodes()
        return self.episode_count

    def __find_episodes(self):
        self.seasons = []
        self.episode_count = 0
        for i in range(0, int(self.season_count)):
            url = site + "?apikey=" + self.omdb.get_api() + "&i=" + self.imdb_id + \
                "&season=" + str(i+1)
            try:
                response = urllib.request.urlopen(url, timeout = 4).read().decode("utf-8")
                json_data = json.loads(response)
                self.seasons.append(omdb_season_data(json_data, i+1))
                self.episode_count += self.seasons[i].episode_count
            except:
                pass

class omdb_season_data:
    def __init__(self, json_data, season_number):
        self.episode_count = len(json_data["Episodes"])
        self.season_number = season_number
        self.episodes = []
        for i in range(0, int(self.episode_count)):
            title = json_data["Episodes"][i]["Title"]
            date = json_data["Episodes"][i]["Released"]
            self.episodes.append(omdb_episode_data(title, i+1, self.season_number, date))

class omdb_episode_data:
    def __init__(self, title, number, season_number, release_date):
        self.number = number
        self.title = title
        self.season_number = season_number
        self.release_date = release_date
    def to_string(self):
        print("S" + "%02d" % self.season_number + "E" + \
            "%02d" % self.number + ": " + self.title + \
            " (" + self.release_date + ")")
