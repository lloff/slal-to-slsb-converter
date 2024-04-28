from marshmallow import ValidationError
from converter.slal.SLALPackSchema import SLALPackSchema
from converter.slal.SLALPack import SLALGroup, SLALPack
from converter.Arguments import Arguments
from converter.animationAnimationSource import AnimationSource
import os
import pathlib
import subprocess
import shutil
import json
import argparse
import json
import re
import pprint

class Loader:

    def load_SLALs(pack: SLALPack):
        for filename in os.listdir(pack.slal_dir):
            path = os.path.join(pack.slal_dir, filename)

            if os.path.isfile(path) and filename.lower().endswith(".json"):
                name = pathlib.Path(filename).stem

                group = SLALGroup(name)

                with open(path, "r") as file:
                    data = json.load(file)

                    schema = SLALPackSchema()
                    try:
                        group.slal_json: SLALPackSchema = schema.load(data)
                    except ValidationError as err:
                        print(err.messages)
                
                pack.groups[group.name] = group



    def load_animation_sources(pack: SLALPack):
        for filename in os.listdir(pack.anim_source_dir):
            print(f"{pack.toString()} | {filename} | Loading animation text file")
            path = os.path.join(pack.anim_source_dir, filename)
            ext = pathlib.Path(filename).suffix
            stem = pathlib.Path(filename).stem

            if os.path.isfile(path) and ext == ".txt":
                with open(path, "r") as file:
                    animation_source = AnimationSource(stem)
                    animation_source.parse(file)

                    group = pack.groups.get(stem)
                    if (group is not None):
                        group.animation_source = animation_source