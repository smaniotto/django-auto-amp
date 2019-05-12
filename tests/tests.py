import re

import pytest

from auto_amp import utils
from test_utils import reload_module, reload_urlconf


@pytest.fixture
def parsed_html():
    """
    Fixture to return a valid and clean HTML document to apply AMP updates individually.
    """
    return utils.parse_html(
        """
        <!doctype hmtl>
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width">
                <title>Page title</title>
            </head>
            <body>
                <h1>Django Auto AMP</h1>
                <p>Generate automatic AMP from your Django templates</p>
            </body>
        </html>
        """
    )


@pytest.fixture
def parsed_html_lean():
    """
    Fixture to return the same HTML content as 'parsed_html' with less initial tags.
    """
    return utils.parse_html(
        """
        <!doctype hmtl>
        <html>
            <head>
                <title>Page title</title>
            </head>
            <body>
                <h1>Django Auto AMP</h1>
                <p>Generate automatic AMP from your Django templates</p>
            </body>
        </html>
        """
    )


def test_canonical_to_amp_path_discovery(client, mocker):
    """
    Asserts that the AMP path directs the user to the correct respective canonical
    path.
    """
    canonical_response = client.get("/")

    mocked_add_amp_tags = mocker.patch("auto_amp.views.add_amp_tags")
    mocked_add_amp_tags.return_value = canonical_response.content

    mocked_website_index = mocker.patch("website.views.index")
    mocked_website_index.return_value = canonical_response
    reload_module("website.urls")
    reload_urlconf()

    amp_response = client.get("/amp/")
    assert amp_response.status_code == 200
    assert mocked_add_amp_tags.call_count == 1
    assert mocked_website_index.call_count == 1


def test_insert_html_amp(parsed_html):
    """
    Asserts that the 'amp' attribute is added to the html tag.
    """
    parsed_amp = utils.insert_html_amp(parsed_html)
    assert parsed_amp.find("html", amp="") is not None


def test_insert_canonical_link(parsed_html):
    """
    Asserts that a link to the canonical path is added to the HTML head.
    """
    path = "/index"
    parsed_amp = utils.insert_canonical_link(parsed_html, path)
    assert parsed_amp.head.find("link", rel="canonical", href=path) is not None


def test_insert_amp_js(parsed_html):
    """
    Asserts that the script tag to load the AMP project JS is added the the HTML head.
    """
    parsed_amp = utils.insert_amp_js(parsed_html)
    assert (
        parsed_amp.head.find("script", src=re.compile("^https://cdn.ampproject.org.*"))
        is not None
    )


def test_insert_charset_meta(parsed_html, parsed_html_lean):
    """
    Asserts that a charset meta tag is added to the HTML head.
    """
    parsed_amp = utils.insert_charset_meta(parsed_html)
    assert parsed_amp.head.find("meta", charset="utf-8") is not None

    parsed_amp_lean = utils.insert_charset_meta(parsed_html_lean)
    assert parsed_amp_lean.head.find("meta", charset="utf-8") is not None


def test_insert_viewport_meta(parsed_html, parsed_html_lean):
    """
    Asserts that the correct viewport meta tag content is added to the HTML head.
    """
    viewport_content = "width=device-width,minimum-scale=1,initial-scale=1"

    parsed_amp = utils.insert_viewport_meta(parsed_html)
    assert (
        parsed_amp.head.find(
            "meta", attrs={"name": "viewport", "content": viewport_content}
        )
        is not None
    )

    parsed_amp_lean = utils.insert_viewport_meta(parsed_html_lean)
    assert (
        parsed_amp_lean.head.find(
            "meta", attrs={"name": "viewport", "content": viewport_content}
        )
        is not None
    )
