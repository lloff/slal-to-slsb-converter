import json
from converter.Arguments import Arguments
from converter.slal.SLALPack import SLALGroup, SLALPack
from converter.slal.SLALPackSchema import ActorSchema, AnimationSchema
import os
import pathlib
import subprocess

class SLALRepairer:

    def repair_slals(pack: SLALPack):
        SLALRepairer._correct_anim_directory(pack)
        SLALRepairer._correct_slal_issues(pack)
        SLALRepairer._export_corrected_slals(pack)

    def _correct_anim_directory(pack:SLALPack):
        group: SLALGroup
        for group in pack.groups.values():
            group.anim_dir_name = group.animation_source.anim_dir
            group.slal_json['name'] = group.animation_source.anim_dir


    def _correct_slal_issues(pack: SLALPack):
        group: SLALGroup
        for group in pack.groups.values():
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
                            actor['type'] = source_actor.gender
            

    def _export_corrected_slals(pack: SLALPack):
        group: SLALGroup
        for group in pack.groups.values():
            path = os.path.join(pack.slal_dir, group.slal_json_filename)

            with open(path, 'w') as f:
                    json.dump(group.slal_json, f, indent=2)