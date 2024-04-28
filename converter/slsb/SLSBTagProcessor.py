from converter.slate.SlateParser import SlateParser
from converter.animation.Stage import ActorStage, AnimationStage
from converter.animation.Actor import Actor
from converter.animation.Animation import Animation
from converter.slal.SLALPack import SLALPack
from converter.slsb.SLSBAnimsSchema import ExtraSchema, PositionExtraSchema, PositionSchema, SexSchema, StageSchema
from converter.Keywords import Keywords
from converter.slsb.Categories import Categories
import os
import shutil

class SLSBTagProcessor:

    def remove_slate_tags(tags, name):
        slate_action_logs = SlateParser.parse()

        if slate_action_logs is not None:
            TagToAdd = ''
            TagToRemove = ''
            for slate_action_log in slate_action_logs:
                for action in slate_action_log.actions:
                    if name.lower() in action['anim'].lower():
                        if action['action'].lower() == 'addtag':
                            TagToAdd = action['tag'].lower()
                            if TagToAdd not in tags:
                                tags.append(TagToAdd)
                        elif action['action'].lower() == 'removetag':
                            TagToRemove = action['tag'].lower()
                            if TagToRemove in tags:
                                tags.remove(TagToRemove)

    def append_missing_tags(tags, stage_name, anim_dir_name):

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['basescale', 'base scale', 'setscale', 'set scale', 'bigguy'], 'scaling')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['femdom', 'amazon', 'femaledomination', 'female domination', 'leito xcross standing'], 'femdom')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['guro', 'execution'], 'gore')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, Keywords.magic, 'magic')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['choke', 'choking'], 'asphyxiation')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['inv'], 'invisfurn')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, Keywords.furni, 'furniture')

        if 'invisfurn' in tags and 'furniture' in tags:
            tags.remove('furniture')
        
        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['facesit'], 'facesitting')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['lotus'], 'lotusposition')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['trib', 'tribbing'], 'tribadism')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['doggystyle', 'doggy'], 'doggy')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['spank'], 'spanking')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['dp', 'doublepen'], 'doublepenetration')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['tp', 'triplepen'], 'triplepenetration')
        
        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['lying', 'laying'], 'triplepenetration')
           
        if 'lying' in tags and 'laying' in tags and 'eggs' not in tags:
            tags.remove('laying')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['rimjob'], 'rimming')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['kiss'], 'kissing')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['hold'], 'holding')

        SLSBTagProcessor._if_then_add(tags, stage_name, anim_dir_name, ['69'], 'sixtynine')

        if '' in tags:
            tags.remove('')

    def _if_then_add(tags: list[str], stage_name:str, anim_dir_name: str, check: list[str], add: str):
        if(add not in tags and any(check in tags) or any(check in stage_name) or any(check in anim_dir_name)):
            tags.append(add)


    def append_missing_slate_tags(tags, stage_num):
        slate_action_logs = SlateParser.parse()

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


    def get_categories(tags: list[str]):
        categories = Categories()

        for tag in tags:
            if tag in Keywords.sub:
                categories.sub = True
                categories.maledom = True
            if tag in Keywords.restraints:
                categories.sub = True
                categories.maledom = True
                categories.restraint = Keywords.restraints[tag]
            if tag in Keywords.femdom:
                categories.maybe_femdom = True
            if tag in Keywords.dead:
                categories.dead = True
            if tag == 'leadin':
                categories.leadin = True
            
        if categories.sub and categories.maybe_femdom:
            categories.maledom = False
            categories.femdom = True

        return categories
    
    def correct_tags(tags):
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
    
    def process_extra(extra: PositionExtraSchema, sex: SexSchema, categories: Categories, first: bool):
        if categories.sub:
            if categories.maledom and sex['female']:
                extra['submissive'] = True
            if categories.maledom and sex['male'] and categories.gay and first:
                extra['submissive'] = True
            if categories.femdom and sex['male']:
                extra['submissive'] = True
            if categories.femdom and sex['female'] and categories.lesbian and first:
                extra['submissive'] = True
            if extra['submissive'] and not categories.applied_restraint:
                categories.applied_restraint = True
                extra[categories.restraint] = True

        if categories.dead and first:
            extra['dead'] = True


   # def process_leadin():
        #if leadin:
        #    for pos in stage['positions']:
        #        pos['strip_data']['default'] = False
        #        pos['strip_data']['helmet'] = True
        #        pos['strip_data']['gloves'] = True


    def process_event(position: PositionSchema, pack: SLALPack):
        event: str = position['event'][0].lower()

        if event in pack.FNIS_data:

            data = pack.FNIS_data[event]

            position['event'][0] = os.path.splitext(data.file_name)[0]

            os.makedirs(os.path.dirname(os.path.join(pack.out_dir, data.out_path)), exist_ok=True)
            
            shutil.copyfile(data.path, os.path.join(pack.out_dir, data.out_path))

            if data.anim_obj is not None:     # The part responsible for AnimObject incorporation
                position['anim_obj'] = ','.join(data.anim_obj)

    def check_toy_tag(stage: StageSchema):
        anim_obj_found = any(pos['anim_obj'] != "" and "cum" not in pos['anim_obj'].lower() for pos in stage['positions'])

        if not anim_obj_found and 'toys' in stage['tags']:
            stage['tags'].remove('toys')
        if anim_obj_found and 'toys' not in stage['tags']:
            stage['tags'].append('toys')



    def process_animation(animation: Animation, categories: Categories, position: PositionSchema, extra: ExtraSchema):
        for key in animation.actors:
            SLSBTagProcessor.process_actor(animation.actors[key], categories, position)

                        
        for key in animation.stages:
            stage = animation.stages[key]
            if stage.name.startswith('Stage'):
                if stage.timer is not None:
                    extra['fixed_len'] = round(float(stage.timer), 2)


    def process_actor(actor: Actor, categories: Categories, position: PositionSchema):
        #if 'object' in actor.args:
            #position['anim_obj'] = actor.args['object'].replace(' ', ',')
        if 'strap_on' in actor.args:
            categories.has_strap_on = True
        if 'sos' in actor.args:
            categories.has_sos_value = True
        #if 'add_cum' in actor.args:
            #has_add_cum = True
        if 'forward' in actor.args:
            position['offset']['x'] = float(actor.args['forward'])
        if 'side' in actor.args:
            position['offset']['y'] = float(actor.args['side'])
        if 'up' in actor.args:
            position['offset']['z'] = float(actor.args['up'])
        if 'rotate' in actor.args:
            position['offset']['r'] = float(actor.args['rotate'])

        if(len(actor.stages) > 0):
            for actor_stage_key in actor.stages:
                if actor_stage_key.startswith('Stage'):
                    stage: ActorStage = actor.stages[actor_stage_key]

                    if stage.strap_on is not False:
                        categories.has_strap_on = True
                    if stage.sos is not None:
                        categories.has_sos_value = True
                    if stage.forward is not None:
                        position['offset']['x'] = stage.forward
                    if stage.side is not None:
                        position['offset']['y'] = stage.side
                    if stage.up is not None:
                        position['offset']['z'] = stage.up
                    if stage.rotate is not None:
                        position['offset']['r'] = stage.rotate
          
                
                
                            

        
