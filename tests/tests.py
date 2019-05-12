import pytest

from auto_amp import utils
from test_utils import reload_module, reload_urlconf


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
