"""
Tests for branca.element
------------------------
"""

from html.parser import HTMLParser

import branca.element as elem


class _IframeAttrs(HTMLParser):
    """Collect the attributes of every <iframe> start tag."""

    def __init__(self):
        super().__init__()
        self.iframes = []

    def handle_starttag(self, tag, attrs):
        if tag == "iframe":
            self.iframes.append(dict(attrs))


def _iframe_attrs(html):
    parser = _IframeAttrs()
    parser.feed(html)
    assert len(parser.iframes) == 1
    return parser.iframes[0]


def test_figure_repr_html_fullscreen_attrs_without_height():
    attrs = _iframe_attrs(elem.Figure()._repr_html_())
    for name in ("allowfullscreen", "webkitallowfullscreen", "mozallowfullscreen"):
        assert name in attrs


def test_figure_repr_html_fullscreen_attrs_with_height():
    # The height branch used to quote the boolean attributes, producing
    # <iframe ... "allowfullscreen" ...>, so the attribute names came out
    # wrapped in literal quotes and the browser ignored them.
    attrs = _iframe_attrs(elem.Figure(height="400px")._repr_html_())
    for name in ("allowfullscreen", "webkitallowfullscreen", "mozallowfullscreen"):
        assert name in attrs, f"{name!r} missing; got {sorted(attrs)}"
    assert attrs["height"] == "400px"
    assert attrs["width"] == "100%"
