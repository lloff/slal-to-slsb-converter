import re

class Actor:
    def __init__(self, number, scene_name):
        self.scene_name = scene_name
        self.number = number
        self.gender: str = None

        self.in_actor = False


    def get_name(self):
        return f"a{self.number}"
        
    def parse_line(self, line):
        if actor_match:= re.search(r'actor\s*(\d+)\s*=\s*([^()]+)\(([^)]*)\)', line):

            if(actor_match.group(1) == self.number):
                self.in_actor = True
                self.gender = actor_match.group(2)

            else:
                self.in_actor = False

