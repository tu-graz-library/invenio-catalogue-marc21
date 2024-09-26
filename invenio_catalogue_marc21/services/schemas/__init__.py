# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module link multiple marc21 modules."""

from invenio_records_marc21.services.schemas import Marc21RecordSchema
from marshmallow_utils.fields import NestedAttribute

from .catalogue import CatalogueSchema


class Marc21CatalogueSchema(Marc21RecordSchema):
    catalogue = NestedAttribute(CatalogueSchema)


__all__ = (
    "CatalogueSchema",
    "Marc21CatalogueSchema",
)
