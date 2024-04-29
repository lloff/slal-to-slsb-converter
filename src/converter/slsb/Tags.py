from typing import Iterable


class Tags:
    def if_then_add(tags: list[str], scene_name:str, anim_dir_name: str, _any: list[str], add: str) -> None:
        if add not in tags and Tags.if_any_in_tags(tags, _any, scene_name, anim_dir_name):
            tags.append(add)

    def if_then_remove(tags: list[str], if_any_are_in: list[str], if_any_are_missing: list[str], remove: str) -> None:
        if  remove in tags and \
            Tags.if_any_in_tags(tags, if_any_are_in ) and \
            not Tags.if_any_in_tags(tags, if_any_are_missing):
            tags.remove(remove)

    def if_any_in_tags(tags: Iterable, _any: list[str], *extra_any: Iterable ) -> bool:
        if  any(item in tags for item in _any) or \
            any(item in extra_check for extra_check in extra_any for item in _any):

            return True
        return False
    
    def get_keyword_in_tags(tags: list[str], keywords: list[str]) -> str:
        return next(item in tags for item in keywords)
    
    def append_unique(list: list[str], add: str) -> None:
        if add not in list:
            list.append(add)