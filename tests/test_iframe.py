# -*- coding: utf-8 -*-

"""
Folium Element Module class IFrame
----------------------
"""

import branca.element as elem

import pytest

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


def test_create_empty_iframe():
    iframe = elem.IFrame()
    iframe.render()


def test_create_iframe():
    iframe = elem.IFrame(html='<p>test content<p>', width=60, height=45)
    iframe.render()


@pytest.mark.headless
def test_rendering_utf8_iframe():
    iframe = elem.IFrame(html=u'<p>Cerrahpaşa Tıp Fakültesi</p>')

    options = Options()
    options.add_argument('-headless')
    driver = Firefox(options=options)

    driver.get('data:text/html,' + iframe.render())
    driver.switch_to.frame(0)
    assert u'Cerrahpaşa Tıp Fakültesi' in driver.page_source
