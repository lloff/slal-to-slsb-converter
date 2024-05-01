from converter.source.SourceParser import AnimationSource
from converter.slal.SLALGroupSchema import SLALGroupSchema
from converter.slsb.SLSBGroupSchema import SLSBGroupchema
from converter.fnis.FNISAnimationStage import FNISAnimationStage
from converter.Arguments import Arguments
import logging
import os

class SLALPack:

    def __init__(self, dir):

        #NOTE: We can't just edit folder names by removing spaces. we have to restore everything back to true name later too
        #Otherwise, no animation files will be found when users generate behaviours because required meshes will be in different folders
        #same applies for animlists and behavoiour file names too

        self.name = dir
        self.working_dir = os.path.join(Arguments.parent_dir, dir)
        self.slal_dir = self.working_dir + "\\SLAnims\\json"

        self.actor_dir = self.working_dir + '\\meshes\\actors'

        self.anim_source_dir = self.working_dir + "\\SLAnims\\source"
        self.no_anim_source = False
        
        self.out_dir = Arguments.parent_dir + "\\conversion\\" + dir.replace(" ", '')

        self.FNIS_data: dict[str, FNISAnimationStage] = dict()

        self.groups: dict[str, PackGroup] = dict()

        logging.getLogger().info(f"{self.toString()} | Found")
        
    
    def validate(self):
        if not os.path.exists(self.slal_dir):
            return False
        if not os.path.exists(self.anim_source_dir):
            self.no_anim_source = True
        if not os.path.exists(self.actor_dir):
            return False
        return True

    def setup(self):
        os.makedirs(self.out_dir + '/SKSE/Sexlab/Registry/Source')

    def toString(self):
        return f"[SLALPack] {self.name}"

     
class PackGroup:
    slal_json: SLALGroupSchema
    slsb_json: SLSBGroupchema
    animation_source: AnimationSource
    
    def __init__(self, name):
        self.name = name
        self.slal_json_filename: str = name + ".json"
        self.slsb_json_filename: str = name + ".slsb.json"

        self.animation_source = None
        self.slal_json = None
        self.slsb_json = None

