from marshmallow import Schema, fields

class ActorStageSchema(Schema):
    id = fields.String(required = True)
    open_mouth = fields.Boolean(required = False)

class ActorSchema(Schema):
    type = fields.String(required = True)
    stages = fields.List(fields.Nested(ActorStageSchema), required = True)
    race = fields.String(required = False)
    add_cum = fields.String(required = False)

class AnimationStageSchema(Schema):
    number = fields.Number(required = True)
    timer = fields.Float(required = True)
    sound = fields.String(required = False)

class AnimationSchema(Schema):
    actors = fields.List(fields.Nested(ActorSchema), required = True)
    creature_race = fields.String(required = True)
    id = fields.String(required = True)
    name = fields.String(required = True)
    sound = fields.String(required = True)
    stages = fields.List(fields.Nested(AnimationStageSchema), required = True)
    tags = fields.String(required = True)

class SLALSchema(Schema):
    animations = fields.List(fields.Nested(AnimationSchema), required = True)
    name = fields.String(required = True)