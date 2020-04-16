# -*- coding: utf-8 -*-
""""
Folium Colormap Module
----------------------
"""
import branca.colormap as cm


def test_simple_step():
    step = cm.StepColormap(
        ["green", "yellow", "red"],
        vmin=3.0,
        vmax=10.0,
        index=[3, 4, 8, 10],
        caption="step",
    )
    step = cm.StepColormap(["r", "y", "g", "c", "b", "m"])
    step._repr_html_()


def test_simple_linear():
    linear = cm.LinearColormap(["green", "yellow", "red"], vmin=3.0, vmax=10.0)
    linear = cm.LinearColormap(
        ["red", "orange", "yellow", "green"], index=[0, 0.1, 0.9, 1.0]
    )
    linear._repr_html_()


def test_linear_to_step():
    some_list = [30.6, 50, 51, 52, 53, 54, 55, 60, 70, 100]
    lc = cm.linear.YlOrRd_06
    lc.to_step(n=12)
    lc.to_step(index=[0, 2, 4, 6, 8, 10])
    lc.to_step(data=some_list, n=12)
    lc.to_step(data=some_list, n=12, method="linear")
    lc.to_step(data=some_list, n=12, method="log")
    lc.to_step(data=some_list, n=30, method="quantiles")
    lc.to_step(data=some_list, quantiles=[0, 0.3, 0.7, 1])
    lc.to_step(data=some_list, quantiles=[0, 0.3, 0.7, 1], round_method="int")
    lc.to_step(data=some_list, quantiles=[0, 0.3, 0.7, 1], round_method="log10")


def test_step_to_linear():
    step = cm.StepColormap(
        ["green", "yellow", "red"],
        vmin=3.0,
        vmax=10.0,
        index=[3, 4, 8, 10],
        caption="step",
    )
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
