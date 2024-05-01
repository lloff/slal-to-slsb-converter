from converter.source.SourceParserActor import Actor
import re

class Animation:
    def __init__(self):
        self.id = None
        self.name = None
        self.actors: dict[str, Actor] = {}

        self.current_actor = None
        self.in_animation = False

    def parse_line(self, line):
        if re.match(r'^\s*Animation\(', line):
            self.in_animation = True

        if re.match(r'^\s*id=', line):
            self.set_id(line) 

        elif re.match(r'^\s*name=', line):
            self.set_name(line)
        
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


    def set_id(self, line):
        self.id = re.search(r'id="([^"]*)"', line).group(1)
    
    def set_name(self, line):
        self.name = re.search(r'name="([^"]*)"', line).group(1)

    def new_actor(self, line):
        actor_match = re.search(r'actor\s*(\d+)\s*=\s*([^()]+)\(([^)]*)\)', line)
        if actor_match:
            actor_number = actor_match.group(1)

            self.current_actor = Actor(actor_number, self.name)
            self.current_actor.parse_line(line)

    def finish_actor(self):
        if self.current_actor:
            self.actors[self.current_actor.get_name()] = self.current_actor

        self.current_actor = False

