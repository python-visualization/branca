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


def test_figure_iframe_title_absent_by_default():
    for height in (None, "400px"):
        attrs = _iframe_attrs(elem.Figure(height=height)._repr_html_())
        assert "title" not in attrs


def test_figure_iframe_title_set():
    for height in (None, "400px"):
        attrs = _iframe_attrs(elem.Figure(height=height, title="My Map")._repr_html_())
        assert attrs["title"] == "My Map"


def test_figure_iframe_title_is_escaped():
    # A title with a double quote must not break out of the attribute.
    attrs = _iframe_attrs(elem.Figure(title='a "b" <c>')._repr_html_())
    assert attrs["title"] == 'a "b" <c>'


def test_iframe_title_absent_by_default():
    for height in (None, "300px"):
        attrs = _iframe_attrs(elem.IFrame("<p>x</p>", height=height).render())
        assert "title" not in attrs


def test_iframe_title_set():
    for height in (None, "300px"):
        attrs = _iframe_attrs(
            elem.IFrame("<p>x</p>", height=height, title="Popup").render(),
        )
        assert attrs["title"] == "Popup"
