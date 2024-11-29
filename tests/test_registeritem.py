from pyge.registeritem import RegisterItem
from pytest import raises


class Doctest(RegisterItem):
    pass


def test_documentation():
    c = Doctest()

    # The plain properties return None if not overridden
    assert c.item_name is None
    assert c.brief is None
    assert c.description is None
    assert c.citation is None
    assert c.general_citation is None
    assert c.authority is None

    # crossref returns a list of strings (or in this case: an empty list)
    assert len(c.crossref) == 0

    # and trying to access a non-existing attribute raises AttributeError
    with raises(AttributeError):
        c.heese == 1
