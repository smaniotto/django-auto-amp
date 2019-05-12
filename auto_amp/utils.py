import re

from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.staticfiles import finders


def add_amp_tags(content, path):
    """
    Adds basic AMP tags to a valid HTML document.
    """
    parsed_amp = parse_html(content)

    parsed_amp = insert_html_amp(parsed_amp)
    parsed_amp = insert_canonical_link(parsed_amp, path)
    parsed_amp = exclude_javascript(parsed_amp)
    parsed_amp = insert_amp_js(parsed_amp)
    parsed_amp = insert_charset_meta(parsed_amp)
    parsed_amp = insert_viewport_meta(parsed_amp)
    parsed_amp = replace_external_stylesheets(parsed_amp)

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


def insert_charset_meta(parsed_amp):
    """
    Inserts a script tag to load the AMP project JS.
    """
    if parsed_amp.find("meta", charset="utf-8"):
        return parsed_amp

    charset_meta = parsed_amp.new_tag("meta", charset="utf-8")
    parsed_amp.head.insert(0, charset_meta)
    return parsed_amp


def insert_viewport_meta(parsed_amp):
    """
    Inserts a new viewport meta tag or update the existing one with the correct
    content.
    """
    viewport_meta = parsed_amp.find("meta", attrs={"name": "viewport"})
    amp_viewport_content = "width=device-width,minimum-scale=1,initial-scale=1"

    if viewport_meta:
        viewport_meta["content"] = amp_viewport_content
    else:
        new_viewport_meta = parsed_amp.new_tag(
            "meta", attrs={"name": "viewport", "content": amp_viewport_content}
        )
        parsed_amp.head.insert(1, new_viewport_meta)

    return parsed_amp


def _fetch_file_content(href):
    """
    Checks whether the href corresponds to a local static file and retrieves its
    content.
    """
    if href.startswith(settings.STATIC_URL):
        static_path = re.sub(f"^{settings.STATIC_URL}", "", href, count=1)
        filesystem_path = finders.find(static_path)
        with open(filesystem_path, "r") as staticfile:
            return staticfile.read()

    # TODO: support third-party stylesheets

    return ""


def replace_external_stylesheets(parsed_amp):
    """
    Finds all stylesheets references, fetch their content and replace with inline
    styles.
    """
    external_stylesheets = parsed_amp.find_all("link", attrs={"rel": "stylesheet"})
    for stylesheet in external_stylesheets:
        css_content = _fetch_file_content(stylesheet["href"])

        stylesheet.extract()

        inline_css = parsed_amp.new_tag("style", attrs={"amp-custom": ""})
        inline_css.string = css_content
        parsed_amp.head.append(inline_css)
    return parsed_amp


def exclude_javascript(parsed_amp):
    """
    Removes all application and third-party JS references. Only allowed text types are
    'application/json' and 'application/ld+json'.
    """
    javascript_tags = parsed_amp.find_all("script")
    javascript_allowed_tags = parsed_amp.find_all(
        "script", attrs={"type": re.compile("^(application/json|application/ld+json)$")}
    )
    for tag in set(javascript_tags) - set(javascript_allowed_tags):
        tag.extract()
    return parsed_amp
