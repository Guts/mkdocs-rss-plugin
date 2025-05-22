from pprint import pprint

import feedparser

rss_source = "https://blog.geotribu.net/feed_rss_created.xml"

feed_parsed = feedparser.parse(rss_source)

# print feed informations
feed = feed_parsed.get("feed")
pprint(feed)

# feed items
for feed_item in feed_parsed.entries:
    pprint(feed_item)
