from converter.animation.source.Stage import ActorStage
import re


class Actor:
    def __init__(self, number):
        self.number = number
        self.stages: dict[str, ActorStage] = {}
        self.type = None
        self.args = {}

        self.current_stage: ActorStage = None
        self.in_actor = False


    def get_name(self):
        return f"a{self.number}"
    
    def finish(self):
        i = 0
        
    def add_stage_line(self, line):
        self.unparsed_stage_lines.append(line)

    def parse_line(self, line):
        if actor_match:= re.search(r'actor\s*(\d+)\s*=\s*([^()]+)\(([^)]*)\)', line):

            if(actor_match.group(1) == self.number):
                self.in_actor = True
                self.type = actor_match.group(2)
                actor_args = actor_match.group(3)

                args = re.findall(r'(\w+)=(?:"([^"]*)"|([^,)]+))', actor_args)

                for arg, value1, value2 in args:
                    value = value1 if value1 else value2
                    self.args[arg] = value
            else:
                self.in_actor = False


        elif stage_match := re.search(r'Stage\((\d+),\s*([^)]*)\)', line):
            if(self.in_actor):
                stage_info = stage_match.groups()
                stage_number = int(stage_info[0])
                stage = ActorStage(stage_number)

                attributes = re.findall(r'(\w+)\s*=\s*("[^"]+"|[^,)]+)', stage_info[1])
                stage.process_attributes(attributes)

                animvars_match = re.search(r'animvars="([^"]*)"', stage_info[1])
                if animvars_match:
                    stage.animvars = animvars_match.group(1)
            
                self.stages[stage.name] = stage

        elif re.search(r'\bstage_params\s*=', line):
            self.in_actor = False

        