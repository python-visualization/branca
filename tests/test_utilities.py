import branca.utilities as ut


def test_color_brewer_base():
    scheme = ut.color_brewer('YlGnBu', 9)
    assert scheme == [
        '#ffffcc', '#d5eeba', '#a3dbb7',
        '#6fc7bd', '#41b6c4', '#269ac1',
        '#1f77b4', '#1c519f', '#0c2c84'
    ]


def test_color_brewer_reverse():
    scheme = ut.color_brewer('YlGnBu')
    scheme_r = ut.color_brewer('YlGnBu_r')
    assert scheme[::-1] == scheme_r
