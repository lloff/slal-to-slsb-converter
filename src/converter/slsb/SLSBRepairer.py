import logging
from converter.slsb.Categories import Categories
from converter.slsb.AnimatorSpecificProcessor import AnimatorSpecificProcessor
from converter.slal.SLALPack import PackGroup, SLALPack
from converter.slsb.SLSBGroupSchema import FurnitureSchema, PositionSchema, SceneSchema, SexSchema, StageSchema
from converter.Arguments import Arguments
from converter.slsb.TagRepairer import TagRepairer

class SLSBRepairer:
    _pack: SLALPack
    _group: PackGroup
    _scene: SceneSchema
    _stage: StageSchema
    _tags: list[str]
    _categories: Categories
    _current_position: PositionSchema

    _tag_repairer: TagRepairer

    def repair(self, pack: SLALPack) -> None:
        self._pack = pack;
        group: PackGroup
        for group in pack.groups.values():

            self._group = group

            logging.getLogger('').info(f"{pack.toString()} | {group.slsb_json_filename} | Editing SLSB Json")

            self._tag_repairer = TagRepairer(pack)

            self._correct()

    def _correct(self) -> None:
        self._group.slsb_json['pack_author'] = Arguments.author

        scenes: dict[str, SceneSchema] = self._group.slsb_json['scenes']

        scene: SceneSchema
        for scene in scenes.values():
            self._scene = scene
    
            stages = self._scene['stages']

            stage: StageSchema
            for stage in stages:
                self._stage = stage
                self._process_stage()


    def _process_stage(self) -> None:
            
            anim_dir = ''
            if (self._group.animation_source is not None):
                anim_dir = self._group.animation_source.anim_dir
            
            self._tags: list[str] = [tag.lower().strip() for tag in self._stage['tags']]

            TagRepairer.remove_slate_tags(self._tags, self._scene['name'])
            TagRepairer.append_missing_tags(self._tags, self._scene['name'], anim_dir)
            TagRepairer.append_missing_slate_tags(self._tags, self._stage['id'])
            TagRepairer.correct_tag_spellings(self._tags)

            positions: list[PositionSchema] = self._stage['positions']

            self._categories = Categories(self._tags, self._scene['name'], anim_dir)

            self._categories.check_anim_object_found(positions)

            TagRepairer.process_anim_object_found(self._tags, self._categories, self._scene['furniture'])

            length = len(positions)

            for i, position in enumerate(positions):
                self._process_position(position, i, length)
        
            self._stage['tags'] = self._tags

    def _process_position(self, position: PositionSchema, scene_name: str, key: int, length: int):
        sex: SexSchema = position['sex']

        TagRepairer.process_extra(position, self._categories, self._tags, key == 0)

        if position['event'] and len(position['event']) > 0:
            first_event_name = position['event'][0].lower()

            TagRepairer.process_event(first_event_name, position, self._pack)
            TagRepairer.correct_futa(first_event_name, sex, key)

            if all(position['race'] != "Vampire Lord" for position in self._stage['positions']):
                TagRepairer.process_vampire(position, first_event_name, self._tags)

        TagRepairer.process_animations(self._pack, scene_name, self._categories, position, self._stage['extra'], self._tags)

        if self._categories.futa:
            AnimatorSpecificProcessor.process_futanari(self._tags, position, key, length)

        if self._categories.scaling:
            AnimatorSpecificProcessor.process_scaling(self._tags, position, scene_name)

        self._categories.update_orientation(sex)
            
