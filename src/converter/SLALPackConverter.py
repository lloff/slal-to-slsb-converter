from converter.slate.SlateParser import SlateParser
from converter.slsb.SLALExportToSLSB import SLALExportToSLSB
from converter.Loader import Loader
from converter.fnis.FNISBehavior import FNISBehavior
from converter.slal.SLALPack import SLALPack
from converter.Arguments import Arguments
from converter.slal.SLALRepairer import SLALRepairer
#from converter.animation.AnimationConverter import AnimationLoader
from converter.fnis.FNISParser import FNISParser
from converter.slsb.SLSBProject import SLSBProject

import os
import pathlib
import subprocess
import shutil
import json
import argparse
import json
import re
import pprint

class SLALPackConverter:

    def start(dir):
        pack = SLALPack(dir);
        if not pack.validate():
            print(f"Pack {pack.toString()} failed validation")
            return;

        pack.setup()

        Loader.load_SLALs(pack)
        Loader.load_animation_sources(pack)
            
        SLALRepairer.repair_slals(pack)

        SLALExportToSLSB.convert_to_slsb(pack)

        FNISParser.convert(pack)

        SLSBProject.build(pack)

        FNISBehavior.build(pack)