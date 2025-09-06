import pytest
from app.app import summarize

@pytest.fixture
def sample():
    return ["1", "2", "3"]

def test_error_tipo_no_lista():
    with pytest.raises(TypeError):
        summarize("no es una lista")

def test_normal(sample):
    result = summarize(sample)
    assert result["count"] == 3
    assert result["sum"] == 6.0
    assert result["avg"] == 2.0

def test_borde_un_elemento():
    result = summarize(["5"])
    assert result["count"] == 1
    assert result["sum"] == 5.0
    assert result["avg"] == 5.0

def test_error_no_numerico():
    with pytest.raises(Exception):
        summarize(["a", "2"])

def test_error_elemento_no_convertible():
    with pytest.raises(ValueError):
        summarize([{}, 2])

def test_error_lista_vacia():
    with pytest.raises(ValueError, match="La lista no debe estar vacía."):
        summarize([])

def test_error_string_no_convertible():
    with pytest.raises(ValueError, match="El elemento en la posición 0 no es convertible a número: a"):
        summarize(["a", "2"])