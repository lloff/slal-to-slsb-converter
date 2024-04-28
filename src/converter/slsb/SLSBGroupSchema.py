from marshmallow import Schema, fields

class ExtraSchema(Schema):
    fixed_len = fields.Float(required = False)
    nav_text = fields.String(required = False)

class OffsetSchema(Schema):
    x = fields.Float(required = True)
    y = fields.Float(required = True)
    z = fields.Float(required = True)
    r = fields.Float(required = True)

class StripDataSchema(Schema):
    default = fields.Boolean(required = True)
    everything = fields.Boolean(required = True)
    nothing = fields.Boolean(required = True)
    helmet = fields.Boolean(required = True)
    gloves = fields.Boolean(required = True)
    boots = fields.Boolean(required = True)

class PositionExtraSchema(Schema):
    submissive = fields.Boolean(required = True)
    vampire = fields.Boolean(required = True)
    climax = fields.Boolean(required = True)
    dead = fields.Boolean(required = True)
    custom = fields.List(fields.Raw(), required = False)

class SexSchema(Schema):
    male = fields.Boolean(required = True)
    female = fields.Boolean(required = True)
    futa = fields.Boolean(required = True)

class PositionSchema(Schema):
    sex = fields.Nested(SexSchema, required = True)
    race = fields.String(required = True)
    event = fields.List(fields.String(), required = True)
    scale = fields.Float(required = True)
    extra = fields.Nested(PositionExtraSchema, required = True)
    offset = fields.Nested(OffsetSchema, required = True)
    anim_obj = fields.String(required = True)
    strip_data = fields.Nested(StripDataSchema, required = True)
    schlong = fields.Integer(required = True)
    

class StageSchema(Schema):
    id = fields.String(required = True)
    name = fields.String(required = True)
    positions = fields.List(fields.Nested(PositionSchema), required = True)
    tags = fields.List(fields.String(), required = True)
    extra = fields.Nested(ExtraSchema, required = False)

class GraphSchema(Schema):
    dest = fields.List(fields.String(), required = True)
    x = fields.Float(required = True)
    y = fields.Float(required = True)

class FurnitureSchema(Schema):
    furni_types = fields.List(fields.String(), required = True)
    allow_bed = fields.Boolean(required = True)
    offset = fields.Nested(OffsetSchema, required = True)

class SceneSchema(Schema):
    id = fields.String(required = True)
    name = fields.String(required = True)
    stages = fields.List(fields.Nested(StageSchema), required = True)
    root = fields.String(required = True)
    graph = fields.Dict(keys=fields.Str(), values=fields.Nested(GraphSchema), required = True)
    furniture = fields.Nested(FurnitureSchema, required = True)
    private = fields.Boolean(required = True)
    has_warnings = fields.Boolean(required = True)

class SLSBGroupchema(Schema):
    pack_name = fields.String(required = True)
    pack_author = fields.String(required = True)
    prefix_hash = fields.String(required = True)
    scenes = fields.Dict(keys=fields.Str(), values=fields.Nested(SceneSchema))