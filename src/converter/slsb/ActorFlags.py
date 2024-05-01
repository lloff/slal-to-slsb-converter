from converter.slsb.SLSBGroupSchema import PositionExtraSchema, PositionSchema, SexSchema
from converter.source.SourceParserActor import Actor
from converter.slsb.Categories import Categories
from converter.slsb.Tags import Tags
import re

class ActorFlags:
    
    def process_submissive(position: PositionSchema, categories: Categories, tags: list[str], first: bool) -> None:
         extra: PositionExtraSchema = position['extra']
         sex = SexSchema = position['sex']

         if categories.submissive:
            if categories.straight and categories.female_count == 1 and 'femdom' not in tags and sex['female']:
                extra['submissive'] = True
            if categories.straight and categories.female_count == 2 and 'femdom' not in tags: #needs_testing
                if sex['female']:
                    extra['submissive'] = True
            if categories.straight and ('femdom' in tags or 'ffffm' in tags) and sex['male']:
                extra['submissive'] = True
            if categories.gay and (('m2m' in tags and categories.male_count == 2 and first) or ('hcos' in tags and (position['race'] == 'Rabbit' or position['race'] == 'Skeever' or position['race'] == 'Horse'))):
                extra['submissive'] = True
            if categories.lesbian and first: # needs_testing
                extra['submissive'] = True

            if categories.sub_categories.unconscious is True and extra['submissive']:
                extra['submissive'] = False
                extra['dead'] = True


    def futa_initial_prep(event_name: str, sex: SexSchema, index: int) -> None:
        if 'kom_futaduo' in event_name:
            sex['female'] = False
            sex['male'] = True

        if 'futafurniture01(bed)' in event_name:
            if index == 0:
                sex['female'] = False
                sex['futa'] = True
            if index == 1:
                sex['male'] = False
                sex['female'] = True


    def process_futa_category(actor: Actor, categories: Categories, sex: SexSchema, tags: list[str]) -> None:  
        if 'anubs' in tags and ('ff' in tags or 'fff' in tags):
            if actor.number in categories.has_schlong:
                sex['female'] = False
                sex['futa'] = True

        if 'flufyfox' in tags:
            if actor.number in categories.has_strap_on:
                sex['female'] = False
                sex['futa'] = True


    def process_futa_posititon(tags: list[str], position: PositionSchema, key: int, length: int):
        sex: SexSchema = position['sex']

        if 'solo' in tags or 'futaall' in tags or ('anubs' in tags and 'mf' in tags) or \
            ('ff' in tags and ('frotting' in tags or 'milking' in tags)):
                sex['female'] = False
                sex['futa'] = True

        if 'billyy' in tags and 'cf' in tags:
            if position['race'] == 'Flame Atronach':
                sex['female'] = False
                sex['futa'] = True
        if 'billyy' in tags and '2futa' in tags and length == 3:
            if key is 0 or key is 1:
                position['sex']['female'] = False
                position['sex']['futa'] = True

        if 'ff' in tags and sex['male']:
            sex['male'] = False
            sex['futa'] = True


    def process_vampire(position: PositionSchema, event_name: str, tags: list[str]) -> None:
        if 'vamp' in event_name and 'vampirelord' not in tags:
                
            if 'vampire' not in tags:
                tags.append('vampire')

            sex: SexSchema = position['sex']
            extra: PositionExtraSchema = position['extra']
            if Tags.if_any_in_tags(tags, ['vampirefemale', 'vampirelesbian', 'femdom', 'cowgirl', 'vampfeedf'], event_name):
                extra['vampire'] = sex['female']
            else:
                extra['vampire'] = sex['male']


    # Not exactly an actor flag but eh! I like it here :)
    def process_scaling(tags: list[str], position: PositionSchema, name:str) -> None:

        pattern_bigguy = re.findall(r'(base\s?scale)\s?(\d+\.\d+)', name.lower())
        for match in pattern_bigguy:
            if match[1] and position['sex']['male']:
                value = float(match[1].replace('"', ''))
                position['scale'] = round(value, 2)          
        pattern_scaling = re.findall(r'(set\s?scale)\s?(\d+(?:\.\d+)?)?', name.lower())
        for match in pattern_scaling:
            if match[1]:
                value = float(match[1].replace('"', ''))
                if 'gs orc' in name.lower() and position['sex']['male']:
                    position['scale'] = round(value, 2)
                if 'gs giantess' in name.lower() and position['sex']['female']:
                    position['scale'] = round(value, 2)
                if 'hcos small' in name.lower() and position['race'] == 'Dragon':
                    position['scale'] = round(value, 2)

