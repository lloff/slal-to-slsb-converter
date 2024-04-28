from converter.animation.AnimationSource import AnimationSource
from converter.slal.SLALPackSchema import SLALPackSchema
from converter.slsb.SLSBAnimsSchema import SLSBPackSchema
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

        self.actor_dir = self.working_dir + '\\meshes\\actors'

        self.animations = {}

        self.FNIS_data: dict[str, FNISAnimationStage] = dict()

        self.groups: dict[str, SLALGroup] = dict()

        print(f"{self.toString()} Found")
        

    def validate(self):
        if not os.path.exists(self.slal_dir):
            return False
        if not os.path.exists(self.anim_source_dir): ##todo does this always exist?
            return False
        if not os.path.exists(self.actor_dir):
            return False
        return True

    def setup(self):
        os.makedirs(self.out_dir + '/SKSE/Sexlab/Registry/Source')

    def toString(self):
        return f"[SLALPack] {self.name}"

    
class SLALGroup:
    slal_json: SLALPackSchema
    slsb_json: SLSBPackSchema
    animation_source: AnimationSource
    anim_dir_name: str
    
    def __init__(self, name):
        self.name = name
        self.slal_json_filename: str = name + ".json"
        self.slsb_json_filename: str = name + ".slsb.json"

