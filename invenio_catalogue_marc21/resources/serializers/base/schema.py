# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024-2025 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
"""Schemas for marc21 records serializers."""


from marshmallow import Schema
from marshmallow.fields import List, String


class CatalogueSchema(Schema):
    """Schema for a catalogue records."""

    root = String()
    parent = String()
    children = List(String())
