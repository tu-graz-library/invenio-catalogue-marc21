# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Schema for marc21 catalogue ui records."""

from functools import partial

from invenio_i18n import get_locale
from marshmallow import Schema, fields
from marshmallow.fields import List
from marshmallow_utils.fields import FormatDate as BaseFormatDatetime
from marshmallow_utils.fields import SanitizedUnicode

from ..fields import MetadataUIField

FormatDatetime = partial(BaseFormatDatetime, locale=get_locale)


class Marc21CatalogueMetadataSchema(Schema):
    """Schema for dumping extra information for the UI."""

    id = SanitizedUnicode(data_key="id", attribute="id")

    additional = (
        # "access",
        # "status",
        # "parent",
        # "links",
        # "files",
        # "is_published",
    )
    links = fields.Dict(attribute="links")
    metadata = MetadataUIField(attribute="metadata")

    created = FormatDatetime(attribute="created", format="medium")

    updated = FormatDatetime(attribute="updated", format="medium")


class Marc21CatalogueSchema(Schema):
    root = fields.Nested(Marc21CatalogueMetadataSchema(), attribute="root")
    parent = fields.Nested(Marc21CatalogueMetadataSchema(), attribute="parent")
    children = List(
        fields.Nested(Marc21CatalogueMetadataSchema()),
        attribute="children",
    )
