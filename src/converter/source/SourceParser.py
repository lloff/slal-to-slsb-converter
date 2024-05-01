from converter.source.SourceParserAnim import Animation
import re

class AnimationSource:
        filename: str = None
        anim_dir: str = None
        anim_name_prefix: str = None

        current_animation = None
        inside_animation = False

        animations: dict[str, Animation] = dict()

        def __init__(self, filename):
            self.filename = filename

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
                self.anim_dir = re.search(r'anim_dir\("([^"]*)"\)', line).group(1)
            elif re.match(r'^\s*anim_name_prefix\("([^"]*)"\)', line):
                self.anim_name_prefix = re.search(r'anim_name_prefix\("([^"]*)"\)', line).group(1)

        def process_animation_start(self, line):
            if re.match(r'^\s*Animation\(', line):
                if self.current_animation:
                    self.finish_current_animation()
                
                self.start_new_animation(line)

        def finish_current_animation(self):
            self.animations[self.get_animation_name(self.current_animation)] = self.current_animation

            self.current_animation = None

        def get_animation_name(self, current_animation: Animation):
            return self.anim_name_prefix + current_animation.name
             
        def start_new_animation(self, line):
            self.current_animation = Animation()
            self.current_animation.parse_line(line)

