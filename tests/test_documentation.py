from pyge import Documentation
from pytest import raises

class Doctest(Documentation):
    pass


def test_documentation():
    c = Doctest()

    # The plain properties return None if not overridden
    assert c.item_name == None
    assert c.brief == None
    assert c.description == None
    assert c.citation == None
    assert c.general_citation == None
    assert c.authority == None

    # crossref returns a list of strings (or in this case: an empty list)
    assert len(c.crossref) == 0

    # and trying to access a non-existing attribute raises AttributeError
    with raises(AttributeError):
        c.heese == 1
