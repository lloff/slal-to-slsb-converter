from converter.fnis.FNISBehavior import FNISBehavior
from converter.SLALPack import SLALPack
from converter.Arguments import Arguments
from converter.SLALConverter import SLALConverter
from converter.animation.AnimationConverter import AnimationConverter
from converter.fnis.FNISConverter import FNISConverter
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

    def convert(dir):
        pack = SLALPack(dir);
        if not pack.validate():
            print(f"Pack {pack.toString()} failed validation")
            return;

        pack.setup()
            
        SLALConverter.convert(pack)

        AnimationConverter.convert(pack)

        FNISConverter.convert(pack)

        SLSBProject.build(pack)

        FNISBehavior.build(pack)