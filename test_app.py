import pytest
from app import classify


def test_low_usage_is_ok():
    assert classify(10) == "OK"


def test_75_is_warning():
    assert classify(75) == "WARNING"


def test_90_is_critical():
    assert classify(90) == "CRITICAL"


def test_invalid_value_raises_error():
    with pytest.raises(ValueError):
        classify(150)
