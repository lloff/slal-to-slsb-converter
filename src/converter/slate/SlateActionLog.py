
class SlateAction:
    def __init__(self, action, anim, tag):
      self.action = action
      self.anim = anim
      self.tag = tag


class SlateActionLog:
    actions: list[SlateAction] = []