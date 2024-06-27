import http.client
import logging
from pathlib import Path

import requests
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache

http.client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
req_log = logging.getLogger("requests.packages.urllib3")
req_log.setLevel(logging.DEBUG)
req_log.propagate = True


sess = CacheControl(
    requests.Session(), cache=FileCache(".web_cache"), cacheable_methods=("HEAD", "GET")
)


# get requests
resp = sess.get("https://geotribu.fr")
resp_img = sess.get(
    "https://cdn.geotribu.fr/img/articles-blog-rdp/capture-ecran/kevish_Air-Traffic.png"
)

# try again, cache hit expected
resp = sess.get("https://geotribu.fr")
resp_img = sess.get(
    "https://cdn.geotribu.fr/img/articles-blog-rdp/capture-ecran/kevish_Air-Traffic.png"
)

# head requests
resp_img = sess.head(
    "https://cdn.geotribu.fr/img/articles-blog-rdp/capture-ecran/kevish_Air-Traffic.png"
)


# try again, cache hit expected
resp_img = sess.head(
    "https://cdn.geotribu.fr/img/articles-blog-rdp/capture-ecran/kevish_Air-Traffic.png"
)

print(list(Path(".web_cache").iterdir()))
