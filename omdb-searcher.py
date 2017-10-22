# -*- coding: utf-8 -*-
import json
import sys
import re   #regex

# Check if string is an IMDB-id
def is_imdb(string):
    re_imdb = re.compile("^tt\d{1,}")
    return True if re_imdb.search(string) else False

if len(sys.argv) < 3:
    print("Missing arguments: search_query and/or api_key")
    sys.exit()
else:
    search_query = sys.argv[1].replace(" ", "+")       #Title or IMDB-id
    api_key = sys.argv[2]

#Valid types: movie, series, episode
search_type = sys.argv[3] if len(sys.argv) > 3 else "movie"
search_year = sys.argv[4] if len(sys.argv) > 4 else "0000"

print(is_imdb(search_query))

print(search_type)
print(search_year)
