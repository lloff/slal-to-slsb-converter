from converter.Arguments import Arguments
from converter.slal.SLALPack import PackGroup, SLALPack
import os
import subprocess
import shutil
import json


class Exporter:

    def convert_slal_to_slsb(pack: SLALPack) -> None:
        print(f"{pack.toString()} | Exporting SLAL json to SLSB...")

        group: PackGroup
        for group in pack.groups.values():
            path = os.path.join(pack.slal_dir, group.slal_json_filename)

            if os.path.isfile(path):
                print(f"{pack.toString()} | {group.name} | Exporting SLAL json to SLSB...")
                output: bytes = subprocess.Popen(f"{Arguments.slsb_path} convert --in \"{path}\" --out \"{Arguments.temp_dir}\"", stdout=subprocess.PIPE).stdout.read()
                to_print: list[str] = output.decode().split("\n")
                [print(f"{pack.toString()} | " + line) for line in to_print]

    def export_corrected_slsbs(pack: SLALPack) -> None:
        print(f"{pack.toString()} | Exporting Corrected SLSBs...")

        group: PackGroup
        for group in pack.groups.values():
            edited_path = Arguments.temp_dir + '/edited/' + group.slsb_json_filename

            with open(edited_path, 'w') as f:
                json.dump(group.slsb_json, f, indent=2)
            
            if not Arguments.no_build:
                output = subprocess.Popen(f"{Arguments.slsb_path} build --in \"{edited_path}\" --out \"{pack.out_dir}\"", stdout=subprocess.PIPE).stdout.read()
                shutil.copyfile(edited_path, pack.out_dir + '/SKSE/Sexlab/Registry/Source/' + group.slsb_json_filename)

                to_print: list[str] = output.decode().split("\n")
                [print(f"{pack.toString()} | " + line) for line in to_print]
