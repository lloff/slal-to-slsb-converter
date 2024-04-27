from converter.animation.source.AnimationFile import AnimationFile
from converter.fnis.FNISAnimationStage import FNISAnimationStage
from converter.Arguments import Arguments
import os

class SLALPack:

    def __init__(self, dir):
        self.name = dir
        self.working_dir = os.path.join(Arguments.parent_dir, dir)
        self.slal_dir = self.working_dir + "\\SLAnims\\json"
        self.anim_source_dir = self.working_dir + "\\SLAnims\\source"
        self.out_dir = Arguments.parent_dir + "\\conversion\\" + dir

        self.anim_dir = self.working_dir + '\\meshes\\actors'

        self.animations = {}

        self.animation_files: list[AnimationFile] = []
        self.FNIS_data: dict[str, FNISAnimationStage] = dict()

        self.anim_json_names = []

        print(f"{self.toString()} Found")
        

    def validate(self):
        if not os.path.exists(self.slal_dir):
            return False
        if not os.path.exists(self.anim_source_dir):
            return False
        if not os.path.exists(self.anim_dir):
            return False
        return True

    def setup(self):
        os.makedirs(self.out_dir + '/SKSE/Sexlab/Registry/Source')

    def toString(self):
        return f"[SLALPack] {self.name}"

    

