import os
import pathlib
import subprocess
import shutil
import json
import argparse
import json
import re
import pprint

from converter.fnis.FNISIterate import FNISIterate
from converter.slal.SLALPack import SLALPack
from converter.Arguments import Arguments

class FNISBehavior:  

    def build(pack: SLALPack):
        print(f"{pack.toString()} Building FNIS behaviors")
        
        if Arguments.fnis_path is not None:
            anim_dir = pack.out_dir + '\\meshes\\actors'
            FNISIterate.iterate_folders(anim_dir, pack, FNISBehavior.edit_output_fnis)
            FNISIterate.iterate_folders(anim_dir, pack, FNISBehavior.build_behavior)

    def build_behavior(parent_dir, list_name, pack: SLALPack):
        list_path = os.path.join(parent_dir, list_name)

        if '_canine' in list_name.lower():
            return

        print('generating', list_path)

        behavior_file_name = list_name.lower().replace('fnis_', '')
        behavior_file_name = behavior_file_name.lower().replace('_list.txt', '')

        behavior_file_name = 'FNIS_' + behavior_file_name + '_Behavior.hkx'

        cwd = os.getcwd()
        os.chdir(Arguments.fnis_path)
        output = subprocess.Popen(f"./commandlinefnisformodders.exe \"{list_path}\"", stdout=subprocess.PIPE).stdout.read()
        #print(output)
        os.chdir(cwd)

        out_path = os.path.normpath(list_path)
        out_path = out_path.split(os.sep)

        start_index = -1
        end_index = -1

        for i in range(len(out_path) - 1, -1, -1):
            split = out_path[i].lower()

            if split == 'meshes':
                start_index = i
            elif split == 'animations':
                end_index = i

        behavior_folder = 'behaviors' if '_wolf' not in list_name.lower() else 'behaviors wolf'

        behavior_path = os.path.join(Arguments.skyrim_path, 'data', *out_path[start_index:end_index], behavior_folder, behavior_file_name)

        if os.path.exists(behavior_path):
            out_behavior_dir = os.path.join(pack.out_dir, *out_path[start_index:end_index], behavior_folder)
            out_behavior_path = os.path.join(out_behavior_dir, behavior_file_name)
            os.makedirs(out_behavior_dir, exist_ok=True)
            shutil.copyfile(behavior_path, out_behavior_path)
        else:
            print(f'WARNING: {behavior_path} not found for {list_path} - please validate behavior file')

        if Arguments.remove_anims:
            for filename in os.listdir(parent_dir):
                if os.path.splitext(filename)[1].lower() == '.hkx':
                    os.remove(os.path.join(parent_dir, filename))
                        
    def edit_output_fnis(file_path, filename, pack):
        full_path = os.path.join(file_path, filename)
        modified_lines = []
        with open(full_path, 'r') as file:
            for line in file:

                line = re.sub(r'b  ', 'b ', line)
                line = re.sub(r'b[ ]*-?a?o,?[ ]+', 'b -o ', line)
                line = re.sub(r'b[ ]*-?a,?[ ]+', 'b ', line)
                line = re.sub(r',', ' ', line)

                modified_lines.append(line)
        with open(full_path, 'w') as file:
            file.writelines(modified_lines)