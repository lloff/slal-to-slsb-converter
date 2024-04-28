from converter.Arguments import Arguments
from converter.slal.SLALPack import PackGroup, SLALPack
from converter.slal.SLALGroupSchema import ActorSchema, AnimationSchema
import os
import pathlib
import subprocess

class SLALExportToSLSB:

    def convert_to_slsb(pack: SLALPack):
        group: PackGroup
        for group in pack.groups.values():
            path = os.path.join(pack.slal_dir, group.slal_json_filename)

            if os.path.isfile(path):
                print(f"{pack.toString()} | {group.name} | Converting SLAL json to SLSB...")
                output = subprocess.Popen(f"{Arguments.slsb_path} convert --in \"{path}\" --out \"{Arguments.temp_dir}\"", stdout=subprocess.PIPE).stdout.read()
