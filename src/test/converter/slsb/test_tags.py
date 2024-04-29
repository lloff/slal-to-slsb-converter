from converter.slsb.Tags import Tags

def test_any_is_in_tags() -> None:
    assert Tags.if_any_in_tags(['banana', 'apple', 'mushroom'], ['mushroom', 'pear']) == True

def test_any_is_in_tags_not() -> None:
    assert Tags.if_any_in_tags(['banana', 'apple', 'mushroom'], ['berry', 'pear']) == False

def test_any_is_in_tags_string() -> None:
    assert Tags.if_any_in_tags(['banana', 'apple', 'mushroom'], ['berry', 'pear'], 'berry is a fruit') == True

def test_any_is_in_tags_lots() -> None:
    assert Tags.if_any_in_tags(['banana', 'apple', 'mushroom'], ['berry', 'pear'], ['trousers', 'monkeys'], 'berry is a fruit', ['hotel', 'apartment']) == True

def test_add_if_in_tags() -> None:
    tags: list[str] = ['banana', 'apple', 'mushroom']
    Tags.if_then_add(tags, 'berry is a fruit', 'melons are nice', ['apple', 'trousers'], 'pear')
    assert  'pear' in tags

def test_add_if_in_string() -> None:
    tags: list[str] = ['banana', 'melon', 'mushroom']
    Tags.if_then_add(tags, 'berry is a fruit', 'apples are nice', ['apple', 'trousers'], 'pear')
    assert  'pear' in tags

def test_remove_if_in_tags() -> None:
    tags: list[str] = ['banana', 'apple', 'mushroom', 'pear']
    Tags.if_then_remove(tags, ['apple', 'trousers'], 'berry is a fruit', 'pear')
    assert  'pear' not in tags

def test_dont_remove_if_in_string() -> None:
    tags: list[str] = ['banana', 'melon', 'mushroom']
    Tags.if_then_remove(tags, ['banana', 'melon'], ['apple', 'trousers'], 'pear')
    assert  'pear' not in tags