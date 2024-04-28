from converter.slal.SLALPack import SLALPack
import os


class FNISIterate:

    def iterate_folders(dir, pack: SLALPack, func):
        anim_dir = os.path.join(dir, 'animations')

        if os.path.exists(anim_dir):
            for filename in os.listdir(anim_dir):
                path = os.path.join(anim_dir, filename)
                
                if os.path.isdir(path):
                    for filename in os.listdir(path):
                        if filename.startswith('FNIS_') and filename.endswith('_List.txt'):
                            func(path, filename, pack)
        else:
            for filename in os.listdir(dir):
                path = os.path.join(dir, filename)

                FNISIterate.iterate_folders(path, pack, func)