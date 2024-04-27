from converter.SLALPack import SLALPack
from converter.Arguments import Arguments
from converter.animation.Metadata import Metadata
from converter.animation.source.AnimationFile import AnimationFile
import os
import pathlib
import subprocess
import shutil
import json
import argparse
import json
import re
import pprint

class AnimationConverter:
    def convert(pack: SLALPack):
        animationFiles = []

        for filename in os.listdir(pack.anim_source_dir):
            print(f"{pack.toString()} | {filename} | Parsing animation text file")
            path = os.path.join(pack.anim_source_dir, filename)
            ext = pathlib.Path(filename).suffix

            if os.path.isfile(path) and ext == ".txt":
                with open(path, "r") as file:
                    animationFile = AnimationFile()
                    animationFile.parse(file)
                    animationFiles.append(animationFile)

        pack.animation_files = animationFiles

