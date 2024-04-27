from converter.animation.source.Stage import AnimationStage
from converter.animation.source.Actor import Actor
import re

class Animation:
    def __init__(self):
        self.id = None
        self.name = None
        self.tags: list[str] = []
        self.sound = None
        self.actors: dict[str, Actor] = {}
        self.stages: dict[str, AnimationStage] = {}

        self.current_actor = None
        self.in_animation = False

    def parse_line(self, line):
        if re.match(r'^\s*Animation\(', line):
            self.in_animation = True

        if re.match(r'^\s*id=', line):
            self.set_id(line) 

        elif re.match(r'^\s*name=', line):
            self.set_name(line)

        elif re.match(r'^\s*tags=', line):
            self.set_tags(line)

        elif re.match(r'^\s*sound=', line):
            self.set_sound(line)
        
        elif self.in_animation and re.match(r'^\s*\)', line):
            self.in_animation = False

        else:
            if self.current_actor:
                self.current_actor.parse_line(line)

                if (self.current_actor.in_actor is False):
                    self.finish_actor()
                    if re.search(r'actor\s*(\d+)\s*=\s*([^()]+)\(([^)]*)\)', line):
                        self.new_actor(line)


            elif re.search(r'actor\s*(\d+)\s*=\s*([^()]+)\(([^)]*)\)', line):
                self.new_actor(line)
            
            if re.search(r'^\s*Stage\(', line):
                if ((self.current_actor is None) or (self.current_actor and self.current_actor.in_actor is False)):
                    self.new_animation_stage(line)

        



    def set_id(self, line):
        self.id = re.search(r'id="([^"]*)"', line).group(1)
    
    def set_name(self, line):
        self.name = re.search(r'name="([^"]*)"', line).group(1)

    def set_tags(self, line):
        self.tags = [tag.strip() for tag in re.search(r'tags="([^"]*)"', line).group(1).split(",")]

    def set_sound(self, line):
        sound_match = re.search(r'sound="([^"]*)"', line)
        if sound_match:
            self.sound = sound_match.group(1)

    def new_actor(self, line):
        actor_match = re.search(r'actor(\d+)=([^()]+)\(([^)]*)\)', line)
        if actor_match:
            actor_number = actor_match.group(1)

            self.current_actor = Actor(actor_number)
            self.current_actor.parse_line(line)

    def finish_actor(self):
        if self.current_actor:
            self.actors[self.current_actor.get_name()] = self.current_actor

        self.current_actor = False

    def new_animation_stage(self, line):
        stage_match = re.search(r'Stage\((\d+)(.*?)\)', line)
        if stage_match:
            stage_info = stage_match.groups()
            stage_number = int(stage_info[0])
            
            stage = AnimationStage(stage_number)

            attributes = re.findall(r'sound=([^"]*)|timer=(-?\d+)', stage_info[1])
            for attr in attributes:
                if attr[0]:
                    stage.sound = attr[0]
                if attr[1]:
                    stage.timer = int(attr[1])

            self.stages[stage.name] = stage