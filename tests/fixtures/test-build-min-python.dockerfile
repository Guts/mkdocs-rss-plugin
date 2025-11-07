# Reference: https://squidfunk.github.io/mkdocs-material/getting-started/#with-docker
FROM python:3.10.19

COPY . .

RUN python3 -m pip install --no-cache-dir -U pip setuptools wheel \
    && python3 -m pip install --no-cache-dir .[docs]

RUN mkdocs build
