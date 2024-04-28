class Tags:
    def _if_then_add(tags: list[str], scene_name:str, anim_dir_name: str, check: list[str], add: str) -> None:
        if add not in tags and Tags._if_in_tags(tags, scene_name, anim_dir_name, check):
            tags.append(add)

    def _if_in_tags(tags: list[str], scene_name:str, anim_dir_name: str, check: list[str]) -> bool:
        if any(item in tags for item in check) or any(item in scene_name for item in check) or any(item in anim_dir_name for item in check):
            return True
        return False