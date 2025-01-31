from flask_resources.parsers import MultiDictSchema
from marshmallow import fields, validate


class CatalogueSearchArgsSchema(MultiDictSchema):
    """Search URL query string arguments."""

    drafts = fields.Bool()