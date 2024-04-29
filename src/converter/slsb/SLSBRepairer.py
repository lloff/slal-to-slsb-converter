from converter.slsb.Categories import Categories
from converter.slsb.AnimatorSpecificProcessor import AnimatorSpecificProcessor
from converter.slal.SLALPack import PackGroup, SLALPack
from converter.slsb.SLSBGroupSchema import FurnitureSchema, PositionSchema, SceneSchema, SexSchema, StageSchema
from converter.Arguments import Arguments
from converter.slsb.TagRepairer import TagRepairer

class SLSBRepairer:
    def repair(pack: SLALPack) -> None:
        group: PackGroup
        for group in pack.groups.values():

            print(f"{pack.toString()} | {group.slsb_json_filename} | Editing SLSB Json")

            SLSBRepairer._correct(group, pack)

    def _correct(group: PackGroup,  pack: SLALPack) -> None:
        group.slsb_json['pack_author'] = Arguments.author

        scenes: dict[str, SceneSchema] = group.slsb_json['scenes']

        scene: SceneSchema
        for scene in scenes.values():
            stages = scene['stages']

            stage: StageSchema
            for stage in stages:
                SLSBRepairer._process_stage(stage, scene['name'], pack, group, scene['furniture'])


    def _process_stage(stage: StageSchema, scene_name: str, pack: SLALPack, group: PackGroup, furniture: FurnitureSchema) -> None:
            
            anim_dir = ''
            if (group.animation_source is not None):
                anim_dir = group.animation_source.anim_dir
            
            tags: list[str] = [tag.lower().strip() for tag in stage['tags']]

            TagRepairer.insert_slate_tags(pack, tags, scene_name)
            TagRepairer.append_missing_tags(tags, scene_name, anim_dir)
            TagRepairer.incorporate_stage_tags(tags, pack, stage['id'])
            TagRepairer.correct_tag_spellings(tags)

            categories: Categories = Categories.get_categories(tags)  

            categories.update_sub_categories(tags, scene_name, anim_dir)
                    
            positions: list[PositionSchema] = stage['positions']

            length = len(positions)

            for i, position in enumerate(positions):
                SLSBRepairer._process_position(position, tags, categories, pack, scene_name, stage, i, length)

            categories.anim_object_found = any(pos['anim_obj'] != "" and "cum" not in pos['anim_obj'].lower() for pos in positions)

            TagRepairer.check_anim_object_found(tags, categories, furniture)
        
            stage['tags'] = tags

    def _process_position(position: PositionSchema, tags: list[str], categories: Categories, pack: SLALPack, scene_name: str, stage: StageSchema, key: int, length: int):
        sex: SexSchema = position['sex']

        TagRepairer.process_extra(position, categories, tags, key == 0)

        if position['event'] and len(position['event']) > 0:
            first_event_name = position['event'][0].lower()

            TagRepairer.process_event(first_event_name, position, pack)
            TagRepairer.correct_futa(first_event_name, sex, key)

            if all(position['race'] != "Vampire Lord" for position in stage['positions']):
                TagRepairer.process_vampire(position, first_event_name, tags)

        TagRepairer.process_animations(pack, scene_name, categories, position, stage['extra'], tags)

        if categories.futa:
            AnimatorSpecificProcessor.process_futanari(tags, position, key, length)

        if categories.scaling:
            AnimatorSpecificProcessor.process_scaling(tags, position, scene_name)

        categories.update_orientation(sex)
            
