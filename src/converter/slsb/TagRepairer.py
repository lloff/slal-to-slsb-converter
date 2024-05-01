from converter.Keywords import Keywords
from converter.slsb.Categories import Categories
from converter.slsb.Tags import Tags

class TagRepairer:

    def append_missing_tags(tags: list[str], scene_name: str, anim_dir_name: str) -> None:

        if '' in tags:
            tags.remove('')

        # tags standardization
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['femdom', 'amazon', 'cowgirl', 'femaledomination', 'female domination', 'leito xcross standing'], 'femdom')
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['basescale', 'base scale', 'setscale', 'set scale', 'bigguy'], 'scaling')
        Tags.if_then_add(tags, scene_name, anim_dir_name, Keywords.magic, 'magic')
        Tags.if_then_remove(tags, ['laying', 'lying'], ['eggs'], 'laying')
        Tags.if_then_remove(tags, ['leadin'], ['asltagged'], 'leadin')
        if any(kwd in tags for kwd in Keywords.leadin_) and all(kwd not in tags for kwd in Keywords.not_leadin):
            tags.append('leadin')
        
        # furniutre tags
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['inv'], 'invisfurn')
        Tags.if_then_add(tags, scene_name, anim_dir_name, Keywords.furniture, 'furniture')
        Tags.if_then_remove(tags, ['invisfurn', 'furniture'], '', 'furniture')

        # official tags
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['guro', 'execution'], 'gore')
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['choke', 'choking'], 'asphyxiation')
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['doggystyle', 'doggy'], 'doggy')
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['facesit'], 'facesitting')
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['lotus'], 'lotusposition')
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['spank'], 'spanking')
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['rimjob'], 'rimming')
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['kiss'], 'kissing')
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['hold'], 'holding')
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['69'], 'sixtynine')
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['trib', 'tribbing'], 'tribadism')
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['dp', 'doublepen'], 'doublepenetration')
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['tp', 'triplepen'], 'triplepenetration')
        
    
    def correct_tag_spellings(tags) -> None:
        for i, tag in enumerate(tags):
            if tag == 'cunnilingius':
                tags[i] = 'cunnilingus'
            if tag == 'agressive':
                tags[i] = 'aggressive'
            if tag == 'femodm':
                tags[i] = 'femdom'
            if tag == 'invfurn':
                tags[i] = 'invisfurn'
            if tag == 'invisible obj':
                tags[i] = 'invisfurn'
            if tag == 'laying' and 'eggs' not in tags:
                tags[i] = 'lying'


    def incorporate_toys_tag(tags: list[str], categories: Categories) -> None:
        if not categories.anim_object_found and 'toys' in tags:
            tags.remove('toys')
        if categories.anim_object_found and 'toys' not in tags:
            tags.append('toys')

