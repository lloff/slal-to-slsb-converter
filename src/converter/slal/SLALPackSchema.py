from marshmallow import Schema, fields

class ActorStageSchema(Schema):
    id = fields.String(required = True)
    open_mouth = fields.Boolean(required = False)
    strap_on = fields.Boolean(required = False)
    silent = fields.Boolean(required = False)
    sos = fields.Integer(required = False)
    up = fields.Float(required = False)
    side = fields.Float(required = False)
    rotate = fields.Float(required = False)
    forward = fields.Float(required = False)

class ActorSchema(Schema):
    type = fields.String(required = True)
    stages = fields.List(fields.Nested(ActorStageSchema), required = True)
    race = fields.String(required = False)
    add_cum = fields.Integer(required = False)

class AnimationStageSchema(Schema):
    number = fields.Number(required = True)
    timer = fields.Float(required = True)
    sound = fields.String(required = False)

class AnimationSchema(Schema):
    actors = fields.List(fields.Nested(ActorSchema), required = True)
    id = fields.String(required = True)
    name = fields.String(required = True)
    sound = fields.String(required = True)
    tags = fields.String(required = True)
    stages = fields.List(fields.Nested(AnimationStageSchema), required = False)
    creature_race = fields.String(required = False)

class SLALPackSchema(Schema):
    animations = fields.List(fields.Nested(AnimationSchema), required = True)
    name = fields.String(required = True)