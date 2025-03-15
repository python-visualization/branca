import pytest

from branca.colormap import _parse_color_as_numerical_sequence


@pytest.mark.parametrize("input_data, expected", [
    ((0, 0, 0), (0.0, 0.0, 0.0, 1.0)),
    ((255, 255, 255), (1.0, 1.0, 1.0, 1.0)),
    ((255, 0, 0), (1.0, 0.0, 0.0, 1.0)),
    ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 1.0)),
    ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5, 1.0)),
    ((0.1, 0.2, 0.3, 0.4), (0.1, 0.2, 0.3, 0.4)),
    ((0.0, 1.0, 0.0, 0.5), (0.0, 1.0, 0.0, 0.5)),
    ((0, 0, 0, 255.0), (0.0, 0.0, 0.0, 1.0)),
    ((0, 0, 255.0, 0.0), (0.0, 0.0, 1.0, 0.0)),
])
def test_parse_color_as_numerical_sequence(input_data, expected):
    assert _parse_color_as_numerical_sequence(input_data) == expected

@pytest.mark.parametrize("input_data, raises", [
    ((256, 0, 0), ValueError),
    ((0, 0, -1), ValueError),
    ((0, 1, 2, 3, 4), ValueError),
    ((0.5, 0.5, 0.5, "string"), TypeError),
])
def test_parse_color_as_numerical_sequence_invalid(input_data, raises):
    with pytest.raises(raises):
        _parse_color_as_numerical_sequence(input_data)
