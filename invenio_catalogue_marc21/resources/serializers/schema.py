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

from marshmallow import Schema


class Marc21CatalogueSchema(Schema):
    """Schema for dumping extra information for the marc21 record."""

    class Meta:
        """Meta class to accept unknown fields."""

        unknown = "include"
