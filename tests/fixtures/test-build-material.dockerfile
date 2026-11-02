# Reference: https://squidfunk.github.io/mkdocs-material/getting-started/#with-docker
FROM jaywhj/mkdocs-materialx

COPY . .

RUN ls -a -r

RUN \
    apk upgrade --update-cache -a \
    && apk add --no-cache --virtual .build gcc musl-dev

RUN python3 -m pip install --no-cache-dir .

RUN apk del .build \
    && rm -rf /tmp/* /root/.cache
