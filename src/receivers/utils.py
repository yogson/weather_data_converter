import re

FILE_URLS_PATTERN = r'href="([^"]*?regular-lat-lon[^"]+\.bz2)"'


def extract_urls_from_html(content: str) -> list[str]:
    return re.findall(FILE_URLS_PATTERN, content)
