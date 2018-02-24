# -*- coding: utf-8 -*-
import json, urllib.request, sys, re, argparse
import omdb

site = "http://www.omdbapi.com"

parser = argparse.ArgumentParser(description='OMDb search')
parser.add_argument('-api', dest='api_key', type=str, help='API key (Required)')
parser.add_argument('query', type=str, help='Search query')
parser.add_argument('-year', dest='search_year', help='Year')
parser.add_argument('-type', dest='search_type', help='get_type: movie, series, episode')
parser.add_argument('-output', dest='output', \
    help='Output: full, full_noep, imdb, title, year, runtime, actors, genre, episode_list, episode_count') # -o works
args = parser.parse_args()

search = omdb.omdb_search(search_string=args.query, search_type=args.search_type, api_key=args.api_key, search_year=args.search_year)

if search.get_json() == None:
    print("Error searching for " + args.query)
    print("String Generated: " + search.get_url())
    sys.exit()
else:
    if search.get_type() is "series":
        data = omdb.omdb_tv_data(search)
    elif search.get_type() is "movie":
        data = omdb.omdb_movie_data(search)
    else:
        print("Could not get type for " + args.query)
        print("String Generated: " + search.get_url())
        sys.exit()

# Output
if args.output == "full" or args.output == "full_noep":
    data.to_string()
    if hasattr(data, 'list_episodes') and args.output != "full_noep":
        print("Episodes (" + str(data.get_episode_count()) + ")")
        data.list_episodes()
elif args.output == "episode_list":
    if hasattr(data, 'list_episodes'):
        data.list_episodes()
    else:
        print("No episodes available for " + data.title)
elif args.output == "episode_count":
    if hasattr(data, 'episode_count'):
        print(data.get_episode_count())
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
elif args.output == "actors":
    print(data.actors)
elif args.output == "runtime":
    print(data.runtime)
else: # No output argument given
    data.to_string()
