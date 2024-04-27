from converter.slsb.AnimatorSpecificProcessor import AnimatorSpecificProcessor
from converter.animationAnimation import Animation
from converter.slal.SLALPack import SLALPack
from converter.slsb.SLSBAnimsSchema import PositionExtraSchema, PositionSchema, SLSBPackSchema, SexSchema, StageSchema
from converter.Arguments import Arguments
from converter.slsb.SLSBProcessor import SLSBProcessor
from marshmallow import ValidationError
import os
import subprocess
import shutil
import json
import json

class SLSBProject:
    def build(pack: SLALPack):
        for filename in pack.anim_json_names:

            filename += ".slsb.json"

            path = os.path.join(Arguments.temp_dir, filename)
            
            if os.path.isdir(path):
                continue

            print(f"{pack.toString()} | {filename} | Editing SLSB Json")

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
                    stages= scene['stages']
                    name = scene['name']
                    for stage in stages:
                        SLSBProject.process_stage(stage, name, pack)
                    
            edited_path = Arguments.temp_dir + '/edited/' + filename

            with open(edited_path, 'w') as f:
                json.dump(slalData, f, indent=2)
            
            if not Arguments.no_build:
                output = subprocess.Popen(f"{Arguments.slsb_path} build --in \"{edited_path}\" --out \"{pack.out_dir}\"", stdout=subprocess.PIPE).stdout.read()
                #print(output)
                shutil.copyfile(edited_path, pack.out_dir + '/SKSE/Sexlab/Registry/Source/' + filename)


    def process_stage(stage: StageSchema, name: str, pack: SLALPack):
            
            tags = [tag.lower().strip() for tag in stage['tags']]

            SLSBProcessor.append_missing_tags(tags, name)
            SLSBProcessor.correct_tags(tags)
            SLSBProcessor.check_toy_tag(stage)

            categories = SLSBProcessor.get_categories(tags)  
                    
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

            categories.has_strap_on = False
            categories.has_sos_value = False
            #categories.has_add_cum = False

            extra = stage['extra']

            for i in range(len(positions)):
                position: PositionSchema = positions[i]
                sex: SexSchema = position['sex']

                position_extra: PositionExtraSchema = position['extra']

                SLSBProcessor.process_extra(position_extra, sex, categories, i == 0)

                if position['event'] and len(position['event']) > 0:
                    SLSBProcessor.process_event(position, pack)

                for file in pack.animation_sources:
                    if name in file.animations:
                        animation: Animation = file.animations[name]
                        SLSBProcessor.process_animation(animation, categories, position, extra)
                    
                if 'futa' in tags or 'futanari' in tags or 'futaxfemale' in tags:
                    AnimatorSpecificProcessor.process_futanari(tags, position, categories, positions)

                if 'bigguy' in tags or 'scaling' in tags:
                    AnimatorSpecificProcessor.process_bigguy(tags, position, name)
        

            stage['tags'] = tags
            
