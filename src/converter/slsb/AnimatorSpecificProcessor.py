from converter.slsb.Categories import Categories
from converter.slsb.SLSBGroupSchema import PositionSchema, SceneSchema, SexSchema
import re

class AnimatorSpecificProcessor:                        

    def process_futanari(tags: list[str], position: PositionSchema, key: int, length: int):
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