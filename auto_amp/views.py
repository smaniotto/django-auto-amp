from django.urls import resolve

from .utils import add_amp_tags


def canonical_to_amp(request, *args, canonical_path="", **kwargs):
    """
    Renders the respective canonical equivalent of the AMP page and add basic AMP tags
    to the content.
    """
    canonical_view, canonical_args, canonical_kwargs = resolve(canonical_path)
    canonical_response = canonical_view(request, *canonical_args, **canonical_kwargs)

    canonical_response.content = add_amp_tags(
        canonical_response.content, canonical_path
    )
    return canonical_response
