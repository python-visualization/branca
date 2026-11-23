"""Tests for accessible HTML attributes."""

import branca.element as elem


def test_iframe_title_is_escaped():
    iframe = elem.IFrame(
        html="<p>test content<p>",
        width=60,
        height=45,
        title='Test "content"',
    )

    assert 'title="Test &quot;content&quot;"' in iframe.render()


def test_figure_accessibility_attributes():
    figure = elem.Figure(title='Map of "places"', lang="fr")

    document = figure.render()
    notebook = figure._repr_html_()

    assert '<html lang="fr">' in document
    assert 'title="Map of &quot;places&quot;"' in notebook
