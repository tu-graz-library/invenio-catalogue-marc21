# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
"""Schemas for marc21 records serializers."""

from invenio_records_marc21.resources.serializers.schema import Marc21Schema
from marshmallow import Schema, fields
from marshmallow_utils.fields import SanitizedUnicode


class CatalogueSchema(Schema):
    """Schema for a catalogue records."""

    root = fields.String(attribute="root")
    parent = fields.String(attribute="parent")
    children = fields.List(fields.String(), attribute="children")


class Marc21CatalogueSchema(Marc21Schema):
    """Schema for dumping extra information for the marc21 record."""

    class Meta:
        """Meta class to accept unknown fields."""

        additional = (
            "access",
            "status",
            "parent",
            "links",
            "files",
            # "is_published",
        )

    catalogue = fields.Nested(CatalogueSchema, attribute="catalogue")
    is_catalogue = fields.Boolean(attribute="is_catalogue")
