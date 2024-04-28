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