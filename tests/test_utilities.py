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
