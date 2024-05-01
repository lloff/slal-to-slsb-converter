from converter.slsb.Categories import Categories
from converter.slal.SLALPack import PackGroup, SLALPack
from converter.slsb.SLSBGroupSchema import FurnitureSchema, PositionSchema, SceneSchema, SexSchema, StageSchema
from converter.Arguments import Arguments
from converter.slsb.TagRepairer import TagRepairer
from converter.slate.SlateTags import SlateTags
from converter.slsb.ActorFlags import ActorFlags
from converter.slsb.StageActorParams import ActorStageParams
import logging
import shutil
import time
import os


class SLSBRepairer:
    start = None

    def repair(pack: SLALPack) -> None:
        group: PackGroup
        for group in pack.groups.values():
            SLSBRepairer.start = time.time()

            logging.getLogger().info(f"{pack.toString()} | {group.slsb_json_filename} | Editing SLSB Json")

            SLSBRepairer._correct(group, pack)


    def _correct(group: PackGroup,  pack: SLALPack) -> None:
        group.slsb_json['pack_author'] = Arguments.author

        scenes: dict[str, SceneSchema] = group.slsb_json['scenes']

        scene: SceneSchema
        for scene in scenes.values():
            stages = scene['stages']

            stage: StageSchema
            for stage in stages:
                SLSBRepairer._process_stage(stage, scene['name'], pack, group, scene['furniture'], scene['has_warnings'])

        total_time = time.time() - SLSBRepairer.start

        logging.getLogger().debug(f"{pack.toString()} | {group.slsb_json_filename} | Editing SLSB Json Took: {round(total_time)}s")



    def _process_stage(stage: StageSchema, scene_name: str, pack: SLALPack, group: PackGroup, furniture: FurnitureSchema, has_warnings: bool) -> None:
            group_name = group.slal_json['name']
            
            tags: list[str] = [tag.lower().strip() for tag in stage['tags']]

            SlateTags.insert_slate_tags(tags, scene_name)
            TagRepairer.append_missing_tags(tags, scene_name, group_name)
            SlateTags.incorporate_stage_tags(tags, pack, stage['id'])
            TagRepairer.correct_tag_spellings(tags)

            categories: Categories = Categories.get_categories(tags, scene_name, group_name)  

            categories.update_sub_categories(tags, scene_name, group_name)
                    
            positions: list[PositionSchema] = stage['positions']

            length = len(positions)

            for i, position in enumerate(positions):
                SLSBRepairer._process_position(position, tags, categories, pack, scene_name, stage, i, length)

            categories.anim_object_found = any(pos['anim_obj'] != "" and "cum" not in pos['anim_obj'].lower() for pos in positions)

            TagRepairer.incorporate_toys_tag(tags, categories)
            TagRepairer.check_anim_object_found(tags, categories, furniture, has_warnings)
        
            stage['tags'] = tags

    def _process_position(position: PositionSchema, tags: list[str], categories: Categories, pack: SLALPack, scene_name: str, stage: StageSchema, key: int, length: int):
        sex: SexSchema = position['sex']

        categories.update_orientation(sex)

        ActorFlags.process_submissive(position, categories, tags, key == 0)

        if position['event'] and len(position['event']) > 0:
            first_event_name = position['event'][0].lower()

            AnimListFixes.correct_event_names(first_event_name, position, pack)
            AnimListFixes.copy_anim_meshes_for_behavior_generation(first_event_name, pack)
            
            ActorStageParams.process_anim_objects
            ActorFlags.futa_initial_prep(first_event_name, sex, key)

            if all(position['race'] != "Vampire Lord" for position in stage['positions']):
                TagRepairer.process_vampire(position, first_event_name, tags)

        TagRepairer.process_animations(pack, scene_name, categories, position, stage['extra'], tags)

        if categories.futa:
            ActorFlags.process_futa_posititon(tags, position, key, length)

        if categories.scaling:
            ActorFlags.process_scaling(tags, position, scene_name)


class AnimListFixes:
    
    def correct_event_names(event_name: str, position: PositionSchema, pack: SLALPack) -> None:
        if event_name in pack.FNIS_data:
            data = pack.FNIS_data[event_name]
            position['event'][0] = os.path.splitext(data.file_name)[0]


    def copy_anim_meshes_for_behavior_generation(event_name: str, pack: SLALPack) -> None:
        if Arguments.skyrim_path:
            if event_name in pack.FNIS_data:
                data = pack.FNIS_data[event_name]
                os.makedirs(os.path.dirname(os.path.join(pack.out_dir, data.out_path)), exist_ok=True)
                shutil.copyfile(data.path, os.path.join(pack.out_dir, data.out_path))

