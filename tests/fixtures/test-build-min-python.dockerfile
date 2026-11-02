# Reference: https://jaywhj.github.io/mkdocs-materialx/installation.html#with-docker
FROM python:3.14.10

COPY . .

RUN python3 -m pip install --no-cache-dir -U pip setuptools wheel \
    && python3 -m pip install --no-cache-dir .[docs,properdocs]

RUN properdocs build
