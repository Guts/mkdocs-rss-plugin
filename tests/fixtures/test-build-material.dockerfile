# Reference: https://squidfunk.github.io/mkdocs-material/getting-started/#with-docker
FROM squidfunk/mkdocs-material

COPY . .

RUN ls

RUN \
  apk upgrade --update-cache -a \
  && apk add --no-cache --virtual .build  build-base

RUN python3 -m pip install --no-cache-dir . \
  && apk del .build \
  && rm -rf /tmp/* /root/.cache
