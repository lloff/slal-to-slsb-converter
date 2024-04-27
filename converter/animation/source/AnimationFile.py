from converter.Arguments import Arguments
from converter.animation.Metadata import Metadata
from converter.animation.source.Animation import Animation
import os
import pathlib
import subprocess
import shutil
import json
import argparse
import json
import re
import pprint

from converter.animation.Metadata import Metadata

class AnimationFile:
        metadata = Metadata()

        current_animation = None
        inside_animation = False

        animations: dict[str, Animation] = dict()

        def parse(self, file):
            for line in file:
                line = line.strip()

                if (self.current_animation):
                     self.current_animation.parse_line(line)

                     if (self.current_animation.in_animation is False):
                        self.finish_current_animation()          
                else:
                    self.parse_line(line)

            if self.current_animation:
                    self.finish_current_animation()


        def parse_line(self, line):
            self.process_metadata(line)
            self.process_animation_start(line)

        def process_metadata(self, line):
            if re.match(r'^\s*anim_dir\("([^"]*)"\)', line):
                self.metadata.anim_dir = re.search(r'anim_dir\("([^"]*)"\)', line).group(1)
            elif re.match(r'^\s*anim_id_prefix\("([^"]*)"\)', line):
                self.metadata.anim_id_prefix = re.search(r'anim_id_prefix\("([^"]*)"\)', line).group(1)
            elif re.match(r'^\s*anim_name_prefix\("([^"]*)"\)', line):
                self.metadata.anim_name_prefix = re.search(r'anim_name_prefix\("([^"]*)"\)', line).group(1)
            elif re.match(r'^\s*common_tags\("([^"]*)"', line):
                self.metadata.common_tags = re.search(r'common_tags\("([^"]*)"', line).group(1)

        def process_animation_start(self, line):
            if re.match(r'^\s*Animation\(', line):
                if self.current_animation:
                    self.finish_current_animation()
                
                self.start_new_animation(line)

        def finish_current_animation(self):
            self.animations[self.get_animation_name(self.current_animation)] = self.current_animation

            self.current_animation = None

        def get_animation_name(self, current_animation):
            return self.metadata.anim_name_prefix + current_animation.name
             
        def start_new_animation(self, line):
            self.current_animation = Animation()
            self.current_animation.parse_line(line)

            
                         

