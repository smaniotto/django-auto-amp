import re

from bs4 import BeautifulSoup


def add_amp_tags(content, path):
    """
    Adds basic AMP tags to a valid HTML document.
    """
    parsed_amp = parse_html(content)

    parsed_amp = insert_html_amp(parsed_amp)
    parsed_amp = insert_canonical_link(parsed_amp, path)
    parsed_amp = insert_amp_js(parsed_amp)

    return str(parsed_amp)


def parse_html(content):
    """
    Parse a HTML document to a Python representation using BeautifulSoup.
    """
    return BeautifulSoup(content, "html.parser")


def insert_html_amp(parsed_amp):
    """
    Inserts the 'amp' attribute to the document's 'html' tag.
    """
    parsed_amp.html["amp"] = ""
    return parsed_amp


def insert_canonical_link(parsed_amp, path):
    """
    Inserts a link to the respetive canonical page.
    """
    canonical_link = parsed_amp.new_tag("link", rel="canonical", href=path)
    parsed_amp.head.append(canonical_link)
    return parsed_amp


def insert_amp_js(parsed_amp):
    """
    Inserts a script tag to load the AMP project JS.
    """
    amp_js = parsed_amp.new_tag(
        "script", src="https://cdn.ampproject.org/v0.js", **{"async": ""}
    )
    parsed_amp.head.append(amp_js)
    return parsed_amp
