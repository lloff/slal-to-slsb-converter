from converter.slal.SLALPack import PackGroup, SLALPack
from converter.slal.SLALGroupSchema import ActorSchema, AnimationSchema
import json
import os

class SLALRepairer:

    def repair(pack: SLALPack):

        #TODO: We shouldn't edit or update the slal jsons unless it is absoltely necessary.

        #changes_made = False
        SLALRepairer._correct_anim_directory(pack)
        SLALRepairer._correct_type_genders(pack)
        #if changes_made:
        SLALRepairer._export_corrected(pack)


    def _correct_anim_directory(pack:SLALPack) -> None:
        group: PackGroup
        for group in pack.groups.values():

            #NOTE: Does this code take into account the instances where there can be multiple source files and slal jsons in a directory too?
            #How does it handle slal json repairing for anim directory name in those instances?

            if pack.no_anim_source:
                if group.slal_json['name'] != pack.name:
                    group.slal_json['name'] = pack.name
                    #changes_made = True
            elif group.animation_source is not None:
                if group.slal_json['name'] != group.animation_source.anim_dir:
                    group.slal_json['name'] = group.animation_source.anim_dir
                    #changes_made = True
            

    def _correct_type_genders(pack: SLALPack):
        group: PackGroup
        for group in pack.groups.values():
            if group.animation_source is not None:
                slal_json = group.slal_json

                animation : AnimationSchema
                for animation in slal_json['animations']:
                    source_animation = group.animation_source.animations.get(animation['name'])

                    if (source_animation is not None):
                        index: int
                        actor: ActorSchema
                        for index, actor in enumerate(animation['actors'], start = 1):
                            source_actor = source_animation.actors.get(f"a{index}")

                            if (source_actor):
                                if actor['type'].lower() == 'type':
                                    actor['type'] = source_actor.gender
                                    #changes_made = True


    def _export_corrected(pack: SLALPack):
        group: PackGroup
        for group in pack.groups.values():
            path = os.path.join(pack.slal_dir, group.slal_json_filename)

            with open(path, 'w') as f:
                    json.dump(group.slal_json, f, indent=2)