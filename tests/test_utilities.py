import branca.utilities as ut

def test_color_brewer_base():
    scheme = ut.color_brewer('YlGnBu')
    scheme = ut.color_brewer('YlGnBu',9)
    
def test_color_brewer_reverse():
    scheme = ut.color_brewer('YlGnBu')
    scheme_r = ut.color_brewer('YlGnBu_r')
    assert scheme[::-1] == scheme_r