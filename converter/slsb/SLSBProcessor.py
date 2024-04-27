from converter.animation.source.Stage import ActorStage, AnimationStage
from converter.animation.source.Actor import Actor
from converter.animation.source.Animation import Animation
from converter.SLALPack import SLALPack
from converter.slsb.SLSBAnimsSchema import ExtraSchema, PositionExtraSchema, PositionSchema, SexSchema, StageSchema
from converter.Keywords import Keywords
from converter.slsb.Categories import Categories
import os
import shutil

class SLSBProcessor:
    def append_missing_tags(tags, name):
        if ('aggressive' in tags or 'aggressivedefault' in tags) and 'forced' not in tags:
            tags.append('forced')
        if 'doggystyle' in tags and 'doggy' not in tags:
            tags.append('doggy')
        if 'lotus' in tags:
            tags.append('lotusposition')
        if '69' in tags:
            tags.append('sixtynine')
        if 'femdom' in tags or 'femaledomination' in tags and 'dominant' not in tags:
            tags.append('dominant')
        if 'conquering' in tags or 'defeated' in tags and 'dominant' not in tags:
            tags.append('dominant')
        if 'facesit' in tags and 'facesitting' not in tags:
            tags.append('facesitting')
        if 'kiss' in tags and 'kissing' not in tags:
            tags.append('kissing')
        if 'hold' in tags and 'holding' not in tags:
            tags.append('holding')
        if 'rimjob' in tags and 'rimming' not in tags:
            tags.append('rimming')
        if 'basescale' in name.lower() or 'base scale' in name.lower()  or 'setscale' in name.lower() or 'set scale' in name.lower():
            tags.append('scaling')
        if 'leadin' in tags:
            tags.remove('leadin')
        if any(kwd in tags for kwd in Keywords.leadin) and all(kwd not in tags for kwd in Keywords.not_leadin):
            tags.append('leadin')


    def get_categories(tags):
        categories = Categories()

        for i in range(len(tags)):
            tag = tags[i]
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
         for i in range(len(tags)):
            tag = tags[i]
            if tag.lower() == 'cunnilingius':
                tags[i] = 'Cunnilingus'
            if tag.lower() == 'guro':
                tags[i] = 'Gore'
    
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
            SLSBProcessor.process_actor(animation.actors[key], categories, position)

                        
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
          
                
                
                            

        
