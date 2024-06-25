import re
from urllib.parse import urljoin

HREF_MATCH_PATTERN = re.compile('href="(.*?)"')
SRC_MATCH_PATTERN = re.compile('src="(.*?)"')


def relative_links_resolve_to_page(page_html, page_url):
    href_links_to_replace = re.findall(HREF_MATCH_PATTERN, page_html)
    src_links_to_replace = re.findall(SRC_MATCH_PATTERN, page_html)
    links_to_replace = set(href_links_to_replace + src_links_to_replace)
    links_with_replacements = [
        (link, urljoin(page_url, link)) for link in links_to_replace
    ]
    replaced_html = page_html
    for original, replacement in links_with_replacements:
        replaced_html = replaced_html.replace(original, replacement)
    return replaced_html


WRAPPER_PATTERNS = [
    re.compile(p, flags=re.DOTALL)
    for p in [
        '<a class="glightbox".*?>(.*?)</a>',
        '<div class="grid cards".*?>(.*?)</div>',
    ]
]


def remove_wrappers(page_html):
    for wrapper_pattern in WRAPPER_PATTERNS:
        page_html = re.sub(wrapper_pattern, r"\1", page_html)
    return page_html
