from converter.slsb.Categories import Categories
from converter.slsb.SLSBGroupSchema import PositionSchema
import re

class AnimatorSpecificProcessor:                        

    def process_futanari(tags: list[str], position: PositionSchema, categories: Categories, positions: list[PositionSchema]):
        sex = position['sex']

        if ('solo' in tags) or ('futaall' in tags) or ('anubs' in tags and 'mf' in tags) or \
            ('ff' in tags and 'frotting' in tags) or ('billyy' in tags and 'cf' in tags):

                if position['race'] == 'Human' and sex['female']:
                    sex['female'] = False
                    sex['futa'] = True

        if 'ff' in tags and sex['male']:
           sex['male'] = False
           sex['futa'] = True

        if 'anubs' in tags and ('ff' in tags or 'fff' in tags):
            for actor_key, actor in position.items():
                if 'sex' in actor_key and actor['female']:
                    if categories.has_sos_value:
                        actor['female'] = False
                        actor['futa'] = True

        if 'billyy' in tags and '2futa' in tags and len(positions) == 3:
            for pos in [positions[0], positions[1]]:
                for actor_key, actor in pos.items():
                    if 'sex' in actor_key and actor['female']:
                        actor['female'] = False
                        actor['futa'] = True

        if 'flufyfox' in tags:
            for actor_key, actor in position.items():
                if 'sex' in actor_key:
                    if categories.has_strap_on:
                        actor['female'] = False
                        actor['futa'] = True

    def process_scaling(tags: list[str], position: PositionSchema, name:str):

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