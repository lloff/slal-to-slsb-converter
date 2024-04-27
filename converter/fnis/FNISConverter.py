from converter.fnis.FNISIterate import FNISIterate
from converter.SLALPack import SLALPack
from converter.fnis.FNISAnimationStage import FNISAnimationStage
import os

class FNISConverter:
            
    def convert(pack: SLALPack):
        for filename in os.listdir(pack.anim_dir):
            print(f"{pack.toString()} | {filename} | Parsing FNIS animation stages")
            path = os.path.join(pack.anim_dir, filename)

            if os.path.isdir(path):
                FNISIterate.iterate_folders(path, pack, FNISConverter.parse_fnis_list)


    def parse_fnis_list(parent_dir, file, pack: SLALPack):
        path = os.path.join(parent_dir, file)

        with open(path) as topo_file:
            previous_stage = None

            for line in topo_file:
                line = line.strip()

                stage: FNISAnimationStage = FNISConverter.parse_fnis_animation_stage(line, parent_dir, previous_stage)

                if(stage):

                    pack.FNIS_data.update({stage.name: stage})

                    if(stage.in_sequence):
                        previous_stage = stage 
                    else:
                        previous_stage = None


    def parse_fnis_animation_stage(line, parent_dir, previous_stage: FNISAnimationStage):
        if len(line) > 0 and line[0] != "'":

            splits = line.split()

            if (len(splits)) == 0 or splits[0].lower() == 'version' or splits[0].lower() == 'ï»¿version':
                return

            anim_file_name = None
            anim_event_name = None
            options = []
            anim_objects = []

            data = FNISAnimationStage()

            for i in range(len(splits)):
                split = splits[i].lower()
                if anim_event_name is not None:
                    anim_objects.append(split)
                if '.hkx' in split:
                    anim_file_name = splits[i]
                    anim_event_name = splits[i - 1]
                if '-' in split:
                    options.append(split)
                    
            anim_event_name = anim_event_name.lower()
            
            anim_path = os.path.join(parent_dir, anim_file_name)
            out_path = os.path.normpath(anim_path)
            out_path = out_path.split(os.sep)

            for i in range(len(out_path) - 1, -1, -1):
                if (out_path[i].lower() == 'meshes'):
                    out_path = out_path[i:]
                    break
        
            out_path = os.path.join('', *out_path)

            if '-a' in line:
                data.in_sequence = True

            data.name = anim_event_name
            data.file_name = anim_file_name
            data.options = options
            data.anim_obj = anim_objects
            data.path = anim_path
            data.out_path = out_path
            
            if (previous_stage is not None):
                previous_stage.sequence.append(data)

            return data
