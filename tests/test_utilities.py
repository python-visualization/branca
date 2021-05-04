import pytest

import branca.utilities as ut


def test_color_brewer_base():
    scheme = ut.color_brewer('YlGnBu', 9)
    assert scheme == [
        '#ffffd9', '#edf8b1', '#c7e9b4',
        '#7fcdbb', '#41b6c4', '#1d91c0',
        '#225ea8', '#253494', '#081d58'
    ]


def test_color_brewer_reverse():
    scheme = ut.color_brewer('YlGnBu')
    scheme_r = ut.color_brewer('YlGnBu_r')
    assert scheme[::-1] == scheme_r


@pytest.mark.parametrize("values,max_labels,expected", [
    ([0, 1, 2, 3, 4], 10, [0, 1, 2, 3, 4]),
    ([0, 1, 2, 3, 4], 2, [0, '', '', 3, '', '']),
    ([3.2, 4.38, 5.56, 6.75, 7.93, 9.11, 10.3], 3, [3.2, '', '', 6.75, '', '', 10.3, '', '']),
    ([0, 1, 2, 3, 4], 4, [0, '', 2, '', 4, '']),
])
def test_legend_scaler(values, max_labels, expected):
    tick_labels = ut.legend_scaler(values, max_labels)
    assert tick_labels == expected
