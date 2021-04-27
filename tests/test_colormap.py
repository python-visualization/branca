# -*- coding: utf-8 -*-
""""
Folium Colormap Module
----------------------
"""
import branca.colormap as cm
import pytest


def test_simple_step():
    step = cm.StepColormap(['green', 'yellow', 'red'],
                           vmin=3., vmax=10.,
                           index=[3, 4, 8, 10], caption='step')
    step = cm.StepColormap(['r', 'y', 'g', 'c', 'b', 'm'])
    step._repr_html_()


def test_simple_linear():
    linear = cm.LinearColormap(['green', 'yellow', 'red'], vmin=3., vmax=10.)
    linear = cm.LinearColormap(['red', 'orange', 'yellow', 'green'],
                               index=[0, 0.1, 0.9, 1.])
    linear._repr_html_()


def test_linear_to_step():
    some_list = [30.6, 50, 51, 52, 53, 54, 55, 60, 70, 100]
    lc = cm.linear.YlOrRd_06
    lc.to_step(n=12)
    lc.to_step(index=[0, 2, 4, 6, 8, 10])
    lc.to_step(data=some_list, n=12)
    lc.to_step(data=some_list, n=12, method='linear')
    lc.to_step(data=some_list, n=12, method='log')
    lc.to_step(data=some_list, n=30, method='quantiles')
    lc.to_step(data=some_list, quantiles=[0, 0.3, 0.7, 1])
    lc.to_step(data=some_list, quantiles=[0, 0.3, 0.7, 1], round_method='int')
    lc.to_step(data=some_list, quantiles=[0, 0.3, 0.7, 1],
               round_method='log10')


def test_step_to_linear():
    step = cm.StepColormap(['green', 'yellow', 'red'],
                           vmin=3., vmax=10.,
                           index=[3, 4, 8, 10], caption='step')
    step.to_linear()


def test_linear_object():
    cm.linear.OrRd_06._repr_html_()
    cm.linear.PuBu_06.to_step(12)
    cm.linear.YlGn_06.scale(3, 12)
    cm.linear._repr_html_()


def test_step_object():
    cm.step.OrRd_06._repr_html_()
    cm.step.PuBu_06.to_linear()
    cm.step.YlGn_06.scale(3, 12)
    cm.step._repr_html_()

@pytest.mark.parametrize("max_labels,expected", [
    (10, [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]),
    (5, [0.0, '', 2.0, '', 4.0, '', 6.0, '', 8.0, '']),
    (3, [0.0, '', '', '', 4.0, '', '', '', 8.0, '', '', '']),
])
def test_max_labels_linear(max_labels, expected):
    colorbar = cm.LinearColormap(['red'] * 10, vmin=0, vmax=9, max_labels=max_labels)
    try:
        colorbar.render()
    except AssertionError: # rendering outside parent Figure raises error
        pass
    assert colorbar.tick_labels == expected


@pytest.mark.parametrize("max_labels,expected", [
    (10, [0.0, '', 2.0, '', 4.0, '', 6.0, '', 8.0, '', 10.0, '']),
    (5, [0.0, '', '', 3.0, '', '', 6.0, '', '', 9.0, '', '']),
    (3, [0.0, '', '', '', 4.0, '', '', '', 8.0, '', '', '']),
])
def test_max_labels_step(max_labels, expected):
    colorbar = cm.StepColormap(['red', 'blue'] * 5, vmin=0, vmax=10, max_labels=max_labels)
    try:
        colorbar.render()
    except AssertionError: # rendering outside parent Figure raises error
        pass
    assert colorbar.tick_labels == expected
