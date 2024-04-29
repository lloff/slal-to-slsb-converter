import logging


class ActorStage:
    sos = None
    strap_on =  False
    silent =  False
    open_mouth =  False
    object =  None
    forward =  None
    side =  None
    up =  None
    rotate =  None
    animvars =  ""
    attributes: dict[str, float] = dict()

    def __init__(self, number):
        self.name = f"Stage {number}"

    def process_attributes(self, attributes):
        for attr, value in attributes:
            if attr == "sos":
                self.sos = int(value)
            elif attr == "strap_on":
                self.strap_on = True
            elif attr == "silent":
                self.silent = True
            elif attr == "open_mouth":
                self.open_mouth = True
            elif attr == "object":
                self.object = value.strip('""')
            elif attr in ["forward", "side", "up", "rotate"]:
                self.attributes[attr] = float(value)
                logging.getLogger().debug(f"{attr}: {self.attributes[attr]}")

class AnimationStage:
    sound = None
    timer = None

    def __init__(self, number):
        self.name = f"Stage {number}"

    