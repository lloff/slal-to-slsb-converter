from converter.slal.SLALPack import PackGroup, SLALPack
from converter.slsb.SLSBGroupSchema import ExtraSchema, FurnitureSchema, PositionExtraSchema, PositionSchema, SceneSchema, SexSchema, StageSchema
from converter.slsb.Categories import Categories
from converter.slsb.Tags import Tags
from converter.Arguments import Arguments
from converter.slsb.ActorFlags import ActorFlags
from converter.Keywords import Keywords


class SceneExtras:

    def leadin_custom_stripping(categories: Categories, position: PositionSchema):
        if Categories.leadin:
            position['strip_data']['default'] = False
            position['strip_data']['helmet'] = True
            position['strip_data']['gloves'] = True


    def allow_bed_for_lying(tags: list[str], categories: Categories, furniture: FurnitureSchema, scene_schema: SceneSchema) -> None:
        if 'lying' in tags and not categories.anim_object_found:
            furniture['allow_bed'] = True
            scene_schema['has_warnings'] = True


    #def specify_furniture_for_scenes(tags: list[str], furniture: FurnitureSchema,):
        #if 'invisfurn' in tags and 'bed' in tags:
        #        furniture['furni_types'] = Keywords.allowed_furnitures['beds']

        #and so on...


class StageParams:

    def process_animations(pack: SLALPack, scene_name: str, categories: Categories, position: PositionSchema, stage_extra: ExtraSchema, tags: list[str]) -> None:
        group: PackGroup
        for group in pack.groups.values():
            if group.animation_source is not None and scene_name in group.animation_source.animations:
                animation: Animation = group.animation_source.animations[scene_name]
                StageParams._process_animation(animation, categories, position, stage_extra, tags)

    def _process_animation(animation: Animation, categories: Categories, position: PositionSchema, stage_extra: ExtraSchema, tags: list[str]) -> None:
        actor: Actor
        for actor in animation.actors.values():
            ActorStageParams.process_actor_stage_params(actor, categories, position, tags)
            ActorFlags.process_futa_category(actor, categories, position['sex'], tags)
            ActorStageParams.process_actor_offsets(actor, categories, position, tags)

        stage: AnimationStage
        for stage in animation.stages.values():
            if stage.name.startswith('Stage'):
                if stage.timer is not None:
                    stage_extra['fixed_len'] = round(float(stage.timer), 2)


class ActorStageParams:

    def process_anim_objects(event_name: str, position: PositionSchema, pack: SLALPack) -> None:
        if event_name in pack.FNIS_data:
            data = pack.FNIS_data[event_name]
            if data.anim_obj is not None: #anim_object incorporation
                position['anim_obj'] = ','.join(data.anim_obj)

    def process_actor_stage_params(actor: Actor, categories: Categories, position: PositionSchema, tags: list[str]) -> None:
        
        if 'strap_on' in actor.args:
            Tags.append_unique(categories.has_strap_on, actor.number)
        if 'sos' in actor.args:
            Tags.append_unique(categories.has_sos_value, actor.number)
        if 'add_cum' in actor.args:
            Tags.append_unique(categories.has_add_cum, actor.number)

        if(len(actor.stages) > 0):
            for stage in actor.stages.values():
                if stage.strap_on is not False:
                    Tags.append_unique(categories.has_strap_on, actor.number)
                if stage.sos is not None:
                    Tags.append_unique(categories.has_sos_value, actor.number)

                ## TODO:
                #has_sos_value = event_key
                #if event_key in has_sos_value and int(event_key[4:]) == stage_num:
                #   pos_num = int(actor_key[1:]) - 1
                #   for pos in [positions[pos_num]]:
                #       pos['schlong'] = source_actor_stage_params['sos']

                ## for futa

                #if has_schlong and actor_key[1:] not in has_schlong:
                #    has_schlong += f",{actor_key[1:]}"
                #else:
                #    has_schlong = actor_key[1:]


    #def process_actor_offsets(actor: Actor, categories: Categories, position: PositionSchema, tags: list[str]) -> None:

                ## TODO:


                #if stage.forward is not None:
                #    position['offset']['x'] = stage.forward
                #if stage.side is not None:
                #    position['offset']['y'] = stage.side
                #if stage.up is not None:
                #    position['offset']['z'] = stage.up
                #if stage.rotate is not None:
                #    position['offset']['r'] = stage.rotate


                #if 'forward' in source_actor_stage_params and source_actor_stage_params['forward'] != 0:
                #     has_forward = event_key
                #     if event_key in has_forward and int(event_key[4:]) == stage_num:
                #         pos_num = int(actor_key[1:]) - 1
                #         for pos in [positions[pos_num]]:
                #             pos['offset']['y'] = source_actor_stage_params['forward']

                #if 'side' in source_actor_stage_params and source_actor_stage_params['side'] != 0:
                #    has_side = event_key
                #    if event_key in has_side and int(event_key[4:]) == stage_num:
                #        pos_num = int(actor_key[1:]) - 1
                #        for pos in [positions[pos_num]]:
                #            pos['offset']['x'] = source_actor_stage_params['side']

                #if 'up' in source_actor_stage_params and source_actor_stage_params['up'] != 0:
                #    has_up = event_key
                #    if event_key in has_up and int(event_key[4:]) == stage_num:
                #        pos_num = int(actor_key[1:]) - 1
                #        for pos in [positions[pos_num]]:
                #            pos['offset']['z'] = source_actor_stage_params['up']

                #if 'rotate' in source_actor_stage_params and source_actor_stage_params['rotate'] != 0:
                #    has_rotate = event_key
                #    if event_key in has_rotate and int(event_key[4:]) == stage_num:
                #        pos_num = int(actor_key[1:]) - 1
                #        for pos in [positions[pos_num]]:
                #            pos['offset']['r'] = source_actor_stage_params['rotate']
