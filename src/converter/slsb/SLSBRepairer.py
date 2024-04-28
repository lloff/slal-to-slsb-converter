from converter.slsb.Categories import Categories
from converter.slsb.AnimatorSpecificProcessor import AnimatorSpecificProcessor
from converter.animation.Animation import Animation
from converter.slal.SLALPack import PackGroup, SLALPack
from converter.slsb.SLSBGroupSchema import PositionExtraSchema, PositionSchema, SceneSchema, SexSchema, StageSchema
from converter.Arguments import Arguments
from converter.slsb.TagRepairer import TagRepairer
import subprocess
import shutil
import json
import os

class SLSBRepairer:
    def repair(pack: SLALPack):
        group: PackGroup
        for group in pack.groups.values():

            print(f"{pack.toString()} | {group.slsb_json_filename} | Editing SLSB Json")

            SLSBRepairer._correct(group, pack)
            SLSBRepairer._export_corrected(group, pack.out_dir)

    def _export_corrected(group: PackGroup, out_dir: str):
        edited_path = Arguments.temp_dir + '/edited/' + group.slsb_json_filename

        with open(edited_path, 'w') as f:
            json.dump(group.slsb_json, f, indent=2)
        
        if not Arguments.no_build:
            output = subprocess.Popen(f"{Arguments.slsb_path} build --in \"{edited_path}\" --out \"{out_dir}\"", stdout=subprocess.PIPE).stdout.read()
            #print(output)
            shutil.copyfile(edited_path, out_dir + '/SKSE/Sexlab/Registry/Source/' + group.slsb_json_filename)



    def _correct(group: PackGroup,  pack: SLALPack) -> None:
        group.slsb_json['pack_author'] = Arguments.author

        scenes: dict[str, SceneSchema] = group.slsb_json['scenes']

        for scene in scenes.values():
            stages = scene['stages']
            scene_name = scene['name']
            for stage in stages:
                SLSBRepairer.process_stage(stage, scene_name, pack, group)


    def process_stage(stage: StageSchema, scene_name: str, pack: SLALPack, group: PackGroup) -> None:
            
            tags = [tag.lower().strip() for tag in stage['tags']]

            TagRepairer.remove_slate_tags(pack, tags, scene_name)
            TagRepairer.append_missing_tags(tags, scene_name, group.anim_dir_name)
            TagRepairer.append_missing_slate_tags(tags, pack, stage['id'])
            TagRepairer.correct_tags(tags)
            TagRepairer.check_toy_tag(stage)

            categories: Categories = Categories.get_categories(tags)  
                    
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

            categories.update_sub_categories(tags, scene_name, group.anim_dir_name)

            for i, position in enumerate(positions):
                SLSBRepairer._process_position(position, tags, categories, pack, scene_name, stage, i == 0)
        
            stage['tags'] = tags

    def _process_position(position: PositionSchema, tags: list[str], categories: Categories, pack: SLALPack, scene_name: str, stage: StageSchema, first: bool):
        sex: SexSchema = position['sex']

        position_extra: PositionExtraSchema = position['extra']

        TagRepairer.process_extra(position_extra, sex, categories, first)

        if position['event'] and len(position['event']) > 0:
            TagRepairer.process_event(position, pack)

        group: PackGroup
        for group in pack.groups.values():
            if scene_name in group.animation_source.animations:
                animation: Animation = group.animation_source.animations[scene_name]
                TagRepairer.process_animation(animation, categories, position, stage['extra'])
            
        if 'futa' in tags or 'futanari' in tags or 'futaxfemale' in tags:
            AnimatorSpecificProcessor.process_futanari(tags, position, categories, stage['positions'])

        if 'bigguy' in tags or 'scaling' in tags:
            AnimatorSpecificProcessor.process_bigguy(tags, position, scene_name)
            
