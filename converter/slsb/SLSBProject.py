from converter.slsb.Categories import Categories
from converter.slsb.AnimatorSpecificProcessor import AnimatorSpecificProcessor
from converter.animation.Animation import Animation
from converter.slal.SLALPack import SLALGroup, SLALPack
from converter.slsb.SLSBAnimsSchema import PositionExtraSchema, PositionSchema, SLSBPackSchema, SexSchema, StageSchema
from converter.Arguments import Arguments
from converter.slsb.SLSBTagProcessor import SLSBTagProcessor
from marshmallow import ValidationError
import os
import subprocess
import shutil
import json
import json

class SLSBProject:
    def build(pack: SLALPack):
        group: SLALGroup
        for group in pack.groups.values():

            path = os.path.join(Arguments.temp_dir, group.slsb_json_filename)
            
            if os.path.isdir(path):
                continue

            print(f"{pack.toString()} | {group.slsb_json_filename} | Editing SLSB Json")

            with open(path, 'r') as f:
                data = json.load(f)

                schema = SLSBPackSchema()
                try:
                    slalData: SLSBPackSchema = schema.load(data)
                except ValidationError as err:
                    print(err.messages)

                scenes = slalData['scenes']
                slalData['pack_author'] = Arguments.author

                for id in scenes:
                    scene = scenes[id]
                    stages = scene['stages']
                    scene_name = scene['name']
                    for stage in stages:
                        SLSBProject.process_stage(stage, scene_name, pack, group)
                    
            edited_path = Arguments.temp_dir + '/edited/' + group.slsb_json_filename

            with open(edited_path, 'w') as f:
                json.dump(slalData, f, indent=2)
            
            if not Arguments.no_build:
                output = subprocess.Popen(f"{Arguments.slsb_path} build --in \"{edited_path}\" --out \"{pack.out_dir}\"", stdout=subprocess.PIPE).stdout.read()
                #print(output)
                shutil.copyfile(edited_path, pack.out_dir + '/SKSE/Sexlab/Registry/Source/' + group.slsb_json_filename)


    def process_stage(stage: StageSchema, scene_name: str, pack: SLALPack, group: SLALGroup):
            
            tags = [tag.lower().strip() for tag in stage['tags']]

            SLSBTagProcessor.remove_slate_tags(pack, tags, scene_name)
            SLSBTagProcessor.append_missing_tags(tags, scene_name, group.anim_dir_name)
            SLSBTagProcessor.append_missing_slate_tags(tags, pack, stage['id'])
            SLSBTagProcessor.correct_tags(tags)
            SLSBTagProcessor.check_toy_tag(stage)

            categories: Categories = SLSBTagProcessor.get_categories(tags)  
                    
            positions = stage['positions'] 

            seen_male = False
            seen_female = False

            for pos in positions:
                sex: SexSchema = pos['sex']
                if sex['male']:
                    seen_male = True
                if sex['female']:
                    seen_female = True

            categories.gay = seen_male and not seen_female
            categories.lesbian = seen_female and not seen_male

            categories.applied_restraint = categories.restraint == ''

            for i, position in enumerate(positions):
                SLSBProject._process_position(position, tags, categories, pack, scene_name, stage, i == 0)
        
            stage['tags'] = tags

    def _process_position(position: PositionSchema, tags: list[str], categories: Categories, pack: SLALPack, scene_name: str, stage: StageSchema, first: bool):
        sex: SexSchema = position['sex']

        position_extra: PositionExtraSchema = position['extra']

        SLSBTagProcessor.process_extra(position_extra, sex, categories, first)

        if position['event'] and len(position['event']) > 0:
            SLSBTagProcessor.process_event(position, pack)

        group: SLALGroup
        for group in pack.groups.values():
            if scene_name in group.animation_source.animations:
                animation: Animation = group.animation_source.animations[scene_name]
                SLSBTagProcessor.process_animation(animation, categories, position, stage['extra'])
            
        if 'futa' in tags or 'futanari' in tags or 'futaxfemale' in tags:
            AnimatorSpecificProcessor.process_futanari(tags, position, categories, stage['positions'])

        if 'bigguy' in tags or 'scaling' in tags:
            AnimatorSpecificProcessor.process_bigguy(tags, position, scene_name)
            
