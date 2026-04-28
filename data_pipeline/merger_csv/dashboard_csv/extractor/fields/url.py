"""
url
---
Resolve the dashboard's ``url`` field for an initiative.

The reference dashboard CSV uses the **slug** form of the public ECI portal
URL, e.g.::

    https://citizens-initiative.europa.eu/initiatives/right2water_en

…whereas the upstream ``eci_initiatives.initiative_url`` column stores the
**registration-number** form, e.g.::

    https://citizens-initiative.europa.eu/initiatives/details/2012/000003_en

The slug is not present in any source CSV — it has to be discovered from
the initiative detail page (typically via the canonical ``<link>`` tag,
breadcrumb, or an HTTP redirect target).

Implementation deliberately omitted — see TODOs.
"""

import logging

logger = logging.getLogger(__name__)


def extract(initiative_url: str) -> str:
    """Return the slug-form public URL for the initiative.

    Args:
        initiative_url: ``eci_initiatives.initiative_url`` value (the
                        ``/initiatives/details/<year>/<number>_<lang>``
                        form).

    Returns:
        Slug-form URL, e.g. ``https://citizens-initiative.europa.eu/initiatives/right2water_en``.

    Raises:
        NotImplementedError: This extractor is a placeholder.
    """
    # TODO: fetch the detail page (or use a cached slug map), read the
    #       canonical link, and return the slug-form URL.
    raise NotImplementedError("url extraction is not implemented yet.")
