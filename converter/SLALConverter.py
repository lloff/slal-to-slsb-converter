from converter.SLALPack import SLALPack
from converter.Arguments import Arguments
import os
import pathlib
import subprocess

class SLALConverter:

    def convert(pack: SLALPack):
        for filename in os.listdir(pack.slal_dir):
            path = os.path.join(pack.slal_dir, filename)

            ext = pathlib.Path(filename).suffix

            json_name = pathlib.Path(filename).stem

            pack.anim_json_names.append(json_name)

            if os.path.isfile(path) and ext == ".json":
                print(f"{pack.toString()} | {json_name} | Converting SLAL json to SLSB...")
                output = subprocess.Popen(f"{Arguments.slsb_path} convert --in \"{path}\" --out \"{Arguments.temp_dir}\"", stdout=subprocess.PIPE).stdout.read()
