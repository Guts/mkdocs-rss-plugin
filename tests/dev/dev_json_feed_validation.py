import json
from pathlib import Path

import jsonfeed as jf
import requests
from jsonfeedvalidator import ErrorTree, format_errors, validate_feed

# read

# Requesting a valid JSON feed!
r = requests.get("https://arxiv-feeds.appspot.com/json/test")
# Parse from raw text...
feed_from_text = jf.Feed.parse_string(r.text)
# ...or parse JSON separately.
r_json = r.json()
feed_from_json = jf.Feed.parse(r_json)

print(feed_from_text.title)

# # write
# me = jf.Author(name="Lukas Schwab", url="https://github.com/lukasschwab")
# feed = jf.Feed("My Feed Title", authors=[me])
# item = jf.Item("some_item_id")
# feed.items.append(item)

# print(feed.toJSON())

# read from file
path_json_feed = Path(__file__).parent.joinpath("json_feed_sample.json")

with path_json_feed.open("r", encoding="UTF-8") as in_json:
    feed_data = json.load(in_json)


feed_from_file = jf.Feed.parse(feed_data)
print(feed_from_file.title)

errors = validate_feed(feed_from_file)
format_errors(feed_from_file, ErrorTree(errors))
