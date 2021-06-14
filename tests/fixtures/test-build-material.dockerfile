# Reference: https://squidfunk.github.io/mkdocs-material/getting-started/#with-docker
FROM squidfunk/mkdocs-material

RUN \
  apk upgrade --update-cache -a \
  && apk add --no-cache --virtual .build  build-base \
  && python3 -m pip install --no-cache-dir mkdocs-rss-plugin \
  && apk del .build \
  && rm -rf /tmp/* /root/.cache
