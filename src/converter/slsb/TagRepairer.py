from converter.slate.SlateParser import SlateParser
from converter.animation.Stage import ActorStage, AnimationStage
from converter.animation.Actor import Actor
from converter.animation.Animation import Animation
from converter.slal.SLALPack import PackGroup, SLALPack
from converter.slsb.SLSBGroupSchema import ExtraSchema, FurnitureSchema, PositionExtraSchema, PositionSchema, SexSchema, StageSchema
from converter.Keywords import Keywords
from converter.slsb.Categories import Categories
from converter.slsb.Tags import Tags
import os
import shutil

class TagRepairer:

    def remove_slate_tags(pack: SLALPack, tags: list[str], stage_name):
        slate_action_logs = SlateParser.parse(pack)

        if slate_action_logs is not None:
            TagToAdd = ''
            TagToRemove = ''
            for slate_action_log in slate_action_logs:
                for action in slate_action_log.actions:
                    if stage_name.lower() in action['anim'].lower():
                        if action['action'].lower() == 'addtag':
                            TagToAdd = action['tag'].lower()
                            if TagToAdd not in tags:
                                tags.append(TagToAdd)
                        elif action['action'].lower() == 'removetag':
                            TagToRemove = action['tag'].lower()
                            if TagToRemove in tags:
                                tags.remove(TagToRemove)

    def append_missing_tags(tags: list[str], scene_name: str, anim_dir_name: str) -> None:

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['basescale', 'base scale', 'setscale', 'set scale', 'bigguy'], 'scaling')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['femdom', 'amazon', 'femaledomination', 'female domination', 'leito xcross standing'], 'femdom')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['guro', 'execution'], 'gore')

        Tags.if_then_add(tags, scene_name, anim_dir_name, Keywords.magic, 'magic')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['choke', 'choking'], 'asphyxiation')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['inv'], 'invisfurn')

        Tags.if_then_add(tags, scene_name, anim_dir_name, Keywords.furniture, 'furniture')

        if 'invisfurn' in tags and 'furniture' in tags:
            tags.remove('furniture')
        
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['facesit'], 'facesitting')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['lotus'], 'lotusposition')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['trib', 'tribbing'], 'tribadism')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['doggystyle', 'doggy'], 'doggy')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['spank'], 'spanking')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['dp', 'doublepen'], 'doublepenetration')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['tp', 'triplepen'], 'triplepenetration')
        
        Tags.if_then_add(tags, scene_name, anim_dir_name, ['lying', 'laying'], 'triplepenetration')
           
        if 'lying' in tags and 'laying' in tags and 'eggs' not in tags:
            tags.remove('laying')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['rimjob'], 'rimming')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['kiss'], 'kissing')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['hold'], 'holding')

        Tags.if_then_add(tags, scene_name, anim_dir_name, ['69'], 'sixtynine')

        if '' in tags:
            tags.remove('')
                

    def append_missing_slate_tags(tags: list[str], pack: SLALPack, stage_num: int):
        slate_action_logs = SlateParser.parse(pack)

        if(slate_action_logs is not None):
            asl_en = str(stage_num) + "en"  # end_stage
            if asl_en in tags:
                stage_num = stage_num - 1
            asl_li = str(stage_num) + "li"  # lead_in
            asl_sb = str(stage_num) + "sb"  # slow_oral
            asl_fb = str(stage_num) + "fb"  # fast_oral
            asl_sv = str(stage_num) + "sv"  # slow_vaginal
            asl_fv = str(stage_num) + "fv"  # fast_vaginal
            asl_sa = str(stage_num) + "sa"  # slow_anal
            asl_fa = str(stage_num) + "fa"  # fast_anal
            asl_sr = str(stage_num) + "sr"  # spit_roast
            asl_dp = str(stage_num) + "dp"  # double_pen
            asl_tp = str(stage_num) + "tp"  # triple_pen

            if (asl_li in tags or asl_sb in tags or asl_fb in tags or asl_sv in tags or asl_fv in tags or asl_sa in tags or asl_fa in tags \
                or asl_sr in tags or asl_dp in tags or asl_tp in tags or asl_en in tags) and 'asltagged' not in tags:
                tags.append('asltagged')

            if 'asltagged' in tags:
                # stores info on vaginal/anal tag presence (for spitroast)
                if 'anal' in tags and 'vaginal' not in tags:
                    tags.append('sranaltmp')
                else:
                    tags.append('srvagtmp')
                # removes all scene tags that would be added by ASL
                if 'leadin' in tags:
                    tags.remove('leadin')
                if 'oral' in tags:
                    tags.remove('oral')
                if 'vaginal' in tags:
                    tags.remove('vaginal')
                if 'anal' in tags:
                    tags.remove('anal')
                if 'spitroast' in tags:
                    tags.remove('spitroast')
                if 'doublepenetration' in tags:
                    tags.remove('doublepenetration')
                if 'triplepenetration' in tags:
                    tags.remove('triplepenetration')
                # each stage tagged differently based on ASL
                if asl_li in tags and 'leadin' not in tags:
                    tags.append('leadin')
                if (asl_sb in tags or asl_fb in tags) and 'oral' not in tags:
                    tags.append('oral')
                if (asl_sv in tags or asl_fv in tags) and 'vaginal' not in tags:
                    tags.append('vaginal')
                if (asl_sa in tags or asl_fa in tags) and 'anal' not in tags:
                    tags.append('anal')
                if asl_sr in tags:
                    if 'spitroast' not in tags:
                        tags.append('spitroast')
                    if 'oral' not in tags:
                        tags.append('oral')
                    if 'sranaltmp' in tags:
                        tags.append('anal')
                    if 'srvagtmp' in tags:
                        tags.append('vaginal')
                if asl_dp in tags:
                    if 'doublepenetration' not in tags:
                        tags.append('doublepenetration')
                    if 'vaginal' not in tags:
                        tags.append('vaginal')
                    if 'anal' not in tags:
                        tags.append('anal')
                if asl_tp in tags:
                    if 'triplepenetration' not in tags:
                        tags.append('triplepenetration')
                    if 'oral' not in tags:
                        tags.append('oral')
                    if 'vaginal' not in tags:
                        tags.append('vaginal')
                    if 'anal' not in tags:
                        tags.append('anal')
                if asl_sb in tags or asl_sv in tags or asl_sa in tags:
                    tags.append('aslslow')
                if asl_fb in tags or asl_fv in tags or asl_fa in tags:
                    tags.append('aslfast')
                if 'sranaltmp' in tags:
                    tags.remove('sranaltmp')
                if 'srvagtmp' in tags:
                    tags.remove('srvagtmp')
        
    
    def correct_tag_spellings(tags):
        for i, tag in enumerate(tags):
            if tag == 'cunnilingius':
                tags[i] = 'cunnilingus'
            if tag == 'agressive':
                tags[i] = 'aggressive'
            if tag == 'femodm':
                tags[i] = 'femdom'
            if tag == 'invfurn':
                tags[i] = 'invisfurn'
            if tag == 'invisible obj':
                tags[i] = 'invisfurn'
            if tag == 'laying' and 'eggs' not in tags:
                tags[i] = 'lying'
    
    def process_extra(position: PositionSchema, categories: Categories, tags: list[str], first: bool) -> None:
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


   # def process_leadin():
        #if leadin:
        #    for pos in stage['positions']:
        #        pos['strip_data']['default'] = False
        #        pos['strip_data']['helmet'] = True
        #        pos['strip_data']['gloves'] = True


    def process_event(event_name: str, position: PositionSchema, pack: SLALPack) -> None:
        if event_name in pack.FNIS_data:

            data = pack.FNIS_data[event_name]

            position['event'][0] = os.path.splitext(data.file_name)[0]

            os.makedirs(os.path.dirname(os.path.join(pack.out_dir, data.out_path)), exist_ok=True)
            
            shutil.copyfile(data.path, os.path.join(pack.out_dir, data.out_path))

            if data.anim_obj is not None:     # The part responsible for AnimObject incorporation
                position['anim_obj'] = ','.join(data.anim_obj)

    def check_anim_object_found(tags: list[str], categories: Categories, furniture: FurnitureSchema) -> None:

        if not categories.anim_object_found and 'toys' in tags:
            tags.remove('toys')
        if categories.anim_object_found and 'toys' not in tags:
            tags.append('toys')   

        if 'lying' in tags and not categories.anim_object_found:
            furniture['allow_bed'] = True

        #if 'invisfurn' in tags:
            #    furniture['furni_types'] = allowed_furnitures['type']
            #    do something...

    def process_vampire(position: PositionSchema, event_name: str, tags: list[str]) -> None:
        if 'vamp' in event_name and 'vampirelord' not in tags:
                
            if 'vampire' not in tags:
                tags.append('vampire')

            sex: SexSchema = position['sex']
            extra: PositionExtraSchema = position['extra']
            if Tags.if_in_tags(tags, event_name, '', ['vampirefemale', 'vampirelesbian', 'femdom', 'cowgirl', 'vampfeedf']):
                extra['vampire'] = sex['female']
            else:
                extra['vampire'] = sex['male']


    def correct_futa(sex: SexSchema, event_name: str, index: int) -> None:
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

    def process_animations(pack: SLALPack, scene_name: str, categories: Categories, position: PositionSchema, stage_extra: ExtraSchema, tags: list[str]) -> None:
        group: PackGroup
        for group in pack.groups.values():
            if group.animation_source is not None and scene_name in group.animation_source.animations:
                animation: Animation = group.animation_source.animations[scene_name]
                TagRepairer._process_animation(animation, categories, position, stage_extra, tags)

    def _process_animation(animation: Animation, categories: Categories, position: PositionSchema, stage_extra: ExtraSchema, tags: list[str]) -> None:
        actor: Actor
        for actor in animation.actors.values():
            TagRepairer.process_actor(actor, categories, position, tags)

        stage: AnimationStage                
        for stage in animation.stages.values():
            if stage.name.startswith('Stage'):
                if stage.timer is not None:
                    stage_extra['fixed_len'] = round(float(stage.timer), 2)


    def process_actor(actor: Actor, categories: Categories, position: PositionSchema, tags: list[str]) -> None:
        
        if 'strap_on' in actor.args:
            Tags.append_unique(categories.has_strap_on, actor.number)
        if 'sos' in actor.args:
            Tags.append_unique(categories.has_sos_value, actor.number)
        if 'add_cum' in actor.args:
            Tags.append_unique(categories.has_add_cum, actor.number)

        if 'forward' in actor.args:
            position['offset']['x'] = float(actor.args['forward'])
        if 'side' in actor.args:
            position['offset']['y'] = float(actor.args['side'])
        if 'up' in actor.args:
            position['offset']['z'] = float(actor.args['up'])
        if 'rotate' in actor.args:
            position['offset']['r'] = float(actor.args['rotate'])

        if(len(actor.stages) > 0):
            for stage in actor.stages.values():
                if stage.strap_on is not False:
                    Tags.append_unique(categories.has_strap_on, actor.number)
                if stage.sos is not None:
                    Tags.append_unique(categories.has_sos_value, actor.number)

                    ## TODO:
                    # has_sos_value = event_key
                     #if event_key in has_sos_value and int(event_key[4:]) == stage_num:
                    #    pos_num = int(actor_key[1:]) - 1
                    #    for pos in [positions[pos_num]]:
                    #        pos['schlong'] = source_actor_stage_params['sos']
                    # for futa
                   # if has_schlong and actor_key[1:] not in has_schlong:
                   #     has_schlong += f",{actor_key[1:]}"
                   # else:
                    #    has_schlong = actor_key[1:]
                

                if stage.forward is not None:
                    position['offset']['x'] = stage.forward
                if stage.side is not None:
                    position['offset']['y'] = stage.side
                if stage.up is not None:
                    position['offset']['z'] = stage.up
                if stage.rotate is not None:
                    position['offset']['r'] = stage.rotate

        TagRepairer._process_actor_futanari(actor, categories, position['sex'], tags)
                    
                ## TODO:
                # if 'forward' in source_actor_stage_params and source_actor_stage_params['forward'] != 0:

                #     has_forward = event_key

                #     if event_key in has_forward and int(event_key[4:]) == stage_num:
                #         pos_num = int(actor_key[1:]) - 1
                #         for pos in [positions[pos_num]]:

                #             pos['offset']['y'] = source_actor_stage_params['forward']
                # if 'side' in source_actor_stage_params and source_actor_stage_params['side'] != 0:
                #     has_side = event_key
                #     if event_key in has_side and int(event_key[4:]) == stage_num:
                #         pos_num = int(actor_key[1:]) - 1
                #         for pos in [positions[pos_num]]:
                #             pos['offset']['x'] = source_actor_stage_params['side']
                # if 'up' in source_actor_stage_params and source_actor_stage_params['up'] != 0:
                #     has_up = event_key
                #     if event_key in has_up and int(event_key[4:]) == stage_num:
                #         pos_num = int(actor_key[1:]) - 1
                #         for pos in [positions[pos_num]]:
                #             pos['offset']['z'] = source_actor_stage_params['up']
                # if 'rotate' in source_actor_stage_params and source_actor_stage_params['rotate'] != 0:
                #     has_rotate = event_key
                #     if event_key in has_rotate and int(event_key[4:]) == stage_num:
                #         pos_num = int(actor_key[1:]) - 1
                #         for pos in [positions[pos_num]]:
                #             pos['offset']['r'] = source_actor_stage_params['rotate']
          
    def _process_actor_futanari(actor: Actor, categories: Categories, sex: SexSchema, tags: list[str]) -> None:  
        if 'anubs' in tags and ('ff' in tags or 'fff' in tags):
            if actor.number in categories.has_schlong:
                sex['female'] = False
                sex['futa'] = True

        if 'flufyfox' in tags:
            if actor.number in categories.has_strap_on:
                sex['female'] = False
                sex['futa'] = True
                            

        
