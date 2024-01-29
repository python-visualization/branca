"""
Folium Element Module class IFrame
----------------------
"""

import os

import pytest
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import branca.element as elem


def test_create_empty_iframe():
    iframe = elem.IFrame()
    iframe.render()


def test_create_iframe():
    iframe = elem.IFrame(html="<p>test content<p>", width=60, height=45)
    iframe.render()


@pytest.mark.headless
def test_rendering_utf8_iframe():
    iframe = elem.IFrame(html="<p>Cerrahpaşa Tıp Fakültesi</p>")

    options = Options()
    options.add_argument("-headless")
    driver = Firefox(options=options)

    driver.get("data:text/html," + iframe.render())
    driver.switch_to.frame(0)
    assert "Cerrahpaşa Tıp Fakültesi" in driver.page_source


@pytest.mark.headless
def test_rendering_figure_notebook():
    """Verify special characters are correctly rendered in Jupyter notebooks."""
    text = '5/7 %, Линейная улица, "\u00e9 Berdsk"'
    figure = elem.Figure()
    elem.Html(text).add_to(figure.html)
    html = figure._repr_html_()

    filepath = "temp_test_rendering_figure_notebook.html"
    filepath = os.path.abspath(filepath)
    with open(filepath, "w") as f:
        f.write(html)

    options = Options()
    options.add_argument("-headless")
    driver = Firefox(options=options)
    try:
        driver.get("file://" + filepath)
        driver.switch_to.frame(0)
        text_div = driver.find_element(By.CSS_SELECTOR, "div")
        assert text_div.text == text
    finally:
        os.remove(filepath)
        driver.quit()
