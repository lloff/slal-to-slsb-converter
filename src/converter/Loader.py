from marshmallow import ValidationError
from converter.slal.SLALGroupSchema import SLALGroupSchema
from converter.slal.SLALPack import PackGroup, SLALPack
from converter.Arguments import Arguments
from converter.animation.AnimationSource import AnimationSource
import os
import pathlib
import subprocess
import shutil
import json
import argparse
import json
import re
import pprint

from converter.slsb.SLSBGroupSchema import SLSBGroupchema

class Loader:

    def load(pack: SLALPack) -> None:
        Loader._init(pack)
        Loader._load_SLALs(pack)
        Loader._load_animation_sources(pack)

    def _init(pack: SLALPack) -> None:
        for filename in os.listdir(pack.slal_dir):
             
            path = os.path.join(pack.slal_dir, filename)

            if os.path.isfile(path) and filename.lower().endswith(".json"):
                name = pathlib.Path(filename).stem

                group = PackGroup(name)

                pack.groups[group.name] = group

        print(f"{pack.toString()} | {len(pack.groups)} Groups Found")


    def _load_SLALs(pack: SLALPack):
        group: PackGroup
        for group in pack.groups.values():

            path = os.path.join(pack.slal_dir, group.slal_json_filename)

            with open(path, "r") as file:
                data = json.load(file)

                schema = SLALGroupSchema()

                try:
                    group.slal_json = schema.load(data)
                except ValidationError as err:
                    print(err.messages)



    def _load_animation_sources(pack: SLALPack):
        print(f"{pack.toString()} | Loading animation source files")
        
        files: list[str] = os.listdir(pack.anim_source_dir)

        group: PackGroup
        for group in pack.groups.values():
            

            filename = group.name + '.txt'
            if filename in files:
                files.remove(filename)
            
            path = os.path.join(pack.anim_source_dir, filename)

            if os.path.isfile(path):
                with open(path, "r") as file:
                    animation_source = AnimationSource(group.name)
                    animation_source.parse(file)

                    group.animation_source = animation_source
            else:
                print(f"{pack.toString()} | {group.name} | WARNING: animation source not found")

        if len(files) > 0:
            print(f"{pack.toString()} | {group.name} | WARNING: Extra animation source files found: {files}")




    def load_SLSBs(pack: SLALPack):
        group: PackGroup
        for group in pack.groups.values():

            path = os.path.join(Arguments.temp_dir, group.slsb_json_filename)

            with open(path, 'r') as file:
                data = json.load(file)

                schema = SLSBGroupchema()
                try:
                    group.slsb_json: SLSBGroupchema = schema.load(data)
                except ValidationError as err:
                    print(err.messages)