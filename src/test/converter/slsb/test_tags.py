from converter.slsb.Tags import Tags

def test_any_is_in_tags() -> None:
    assert Tags.if_in_tags(['banana', 'apple', 'mushroom'], ['mushroom', 'pear']) == True

def test_any_is_in_tags_not() -> None:
    assert Tags.if_in_tags(['banana', 'apple', 'mushroom'], ['berry', 'pear']) == False

def test_any_is_in_tags_string() -> None:
    assert Tags.if_in_tags(['banana', 'apple', 'mushroom'], ['berry', 'pear'], 'berry is a fruit') == True