import pytest

from branca.colormap import (
    _color_float_to_int,
    _color_int_to_float,
    _is_hex,
    _parse_color,
    _parse_color_as_numerical_sequence,
    _parse_hex,
)


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ((255, 0, 0), (1.0, 0.0, 0.0, 1.0)),
        ((255, 0, 0, 127), (1.0, 0.0, 0.0, 0.4980392156862745)),
        ("#FF0000", (1.0, 0.0, 0.0, 1.0)),
        ("red", (1.0, 0.0, 0.0, 1.0)),
        ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5, 1.0)),
        ((0.25, 0.5, 0.75), (0.25, 0.5, 0.75, 1.0)),
        ((0.1, 0.2, 0.3, 0.4), (0.1, 0.2, 0.3, 0.4)),
        ("#0000FF", (0.0, 0.0, 1.0, 1.0)),
        ("#00FF00", (0.0, 1.0, 0.0, 1.0)),
        ("#FFFFFF", (1.0, 1.0, 1.0, 1.0)),
        ("#000000", (0.0, 0.0, 0.0, 1.0)),
        ("#808080", (0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1.0)),
        (
            "#1A2B3C",
            (0.10196078431372549, 0.16862745098039217, 0.23529411764705882, 1.0),
        ),
        ("green", (0.0, 0.5019607843137255, 0.0, 1.0)),
    ],
)
def test_parse_color(input_data, expected):
    assert _parse_color(input_data) == expected


@pytest.mark.parametrize(
    "input_data, expected",
    [
        # these are byte values as ints and should be normalized and converted
        ((0, 0, 0), (0.0, 0.0, 0.0, 1.0)),
        ((255, 255, 255), (1.0, 1.0, 1.0, 1.0)),
        ((255, 0, 0), (1.0, 0.0, 0.0, 1.0)),
        # a special case: ints that are 0 or 1 should be considered bytes
        ((0, 0, 1), (0.0, 0.0, 1 / 255, 1.0)),
        ((0, 0, 0, 1), (0.0, 0.0, 0.0, 1 / 255)),
        # these already are normalized floats
        ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 1.0)),
        ((0.0, 0.0, 1.0), (0.0, 0.0, 1.0, 1.0)),
        ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5, 1.0)),
        ((0.1, 0.2, 0.3, 0.4), (0.1, 0.2, 0.3, 0.4)),
        ((0.0, 1.0, 0.0, 0.5), (0.0, 1.0, 0.0, 0.5)),
        # these are byte values as floats and should be normalized
        ((0, 0, 0, 255.0), (0.0, 0.0, 0.0, 1.0)),
        ((0, 0, 255.0, 0.0), (0.0, 0.0, 1.0, 0.0)),
        # if floats and ints are mixed, assume they are intended as floats
        ((0, 0, 1.0), (0.0, 0.0, 1.0, 1.0)),
        # unless some of them are between 1 and 255
        ((0, 0, 1.0, 128), (0.0, 0.0, 1 / 255, 128 / 255)),
    ],
)
def test_parse_color_as_numerical_sequence(input_data, expected):
    assert _parse_color_as_numerical_sequence(input_data) == expected


@pytest.mark.parametrize(
    "input_data, raises",
    [
        # larger than 255
        ((256, 0, 0), ValueError),
        # smaller than 0
        ((0, 0, -1), ValueError),
        # sequence too long
        ((0, 1, 2, 3, 4), ValueError),
        # sequence too short
        ((0, 1), ValueError),
        # invalid type in sequence
        ((0.5, 0.5, 0.5, "string"), TypeError),
    ],
)
def test_parse_color_as_numerical_sequence_invalid(input_data, raises):
    with pytest.raises(raises):
        _parse_color_as_numerical_sequence(input_data)


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("#123456", True),
        ("#abcdef", True),
        ("#ABCDEF", True),
        ("#1A2B3C", True),
        ("#123", False),
        ("123456", False),
        ("#1234567", False),
    ],
)
def test_is_hex(input_data, expected):
    assert _is_hex(input_data) == expected


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("#000000", (0.0, 0.0, 0.0, 1.0)),
        ("#FFFFFF", (1.0, 1.0, 1.0, 1.0)),
        ("#FF0000", (1.0, 0.0, 0.0, 1.0)),
        ("#00FF00", (0.0, 1.0, 0.0, 1.0)),
        ("#0000FF", (0.0, 0.0, 1.0, 1.0)),
        ("#808080", (0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1.0)),
    ],
)
def test_parse_hex(input_data, expected):
    assert _parse_hex(input_data) == expected


@pytest.mark.parametrize(
    "input_data, expected",
    [
        (0, 0.0),
        (255, 1.0),
        (128, 0.5019607843137255),
        (64, 0.25098039215686274),
        (192, 0.7529411764705882),
    ],
)
def test_color_byte_to_normalized_float(input_data, expected):
    assert _color_int_to_float(input_data) == expected


@pytest.mark.parametrize(
    "input_data, expected",
    [
        (0.0, 0),
        (0.5, 127),
        (1.0, 255),
        (0.9999, 255),
        (0.1, 25),
        (0.75, 191),
    ],
)
def test_color_normalized_float_to_byte_int(input_data, expected):
    assert _color_float_to_int(input_data) == expected
