# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Metadata field for marc21 records."""

import re

from invenio_i18n import gettext as _
from invenio_records_marc21.records.fields.resourcetype import ResourceTypeEnum
from invenio_records_marc21.resources.serializers.ui.fields.metadata import Marc21Fields
from marshmallow.fields import Field


class MetadataUIField(Field):
    """Schema for the record metadata."""

    def _serialize(self, value, attr, obj, **kwargs):
        """Serialise access status."""
        fields = Marc21Fields(value.get("fields", {}))
        out = {}

        if not fields:
            return out

        return {
            "languages": fields.get_values("041", subfield_notation="a"),
            "authors": self.get_authors(fields),
            "titles": self.get_titles(fields),
            "copyright": fields.get_values("264"),
            "description": self.get_description(fields),
            "notes": fields.get_values("500"),
            "resource_type": self.get_resource_type(fields),
            "published": self.get_published_month(fields),
        }

    def get_authors(self, fields):
        """Get authors."""
        authors = []

        if "100" in fields:
            authors += fields.get_subfields("100", subfield_notations=["a", "8"])

        if "700" in fields:
            authors += fields.get_subfields("700", subfield_notations=["a", "8"])

        return authors

    def get_titles(self, fields):
        """Get title.

        The normal separator between the main title and the additional
        title is ':'.

        There are special cases where the 245 subfield 'b' has a '='
        in front. If this happens the separator between 'a' and 'b'
        should not be ':' because there is already the '=' as a
        separator.
        """
        titles = fields.get_values("245", subfield_notation="a")
        additional_titles = fields.get_values("245", subfield_notation="b")

        if len(additional_titles) > 0 and additional_titles[0][0] != "=":
            titles += [":"]

        titles += additional_titles

        return [re.sub(r"[<>]", "", title) for title in titles]

    def get_published_month(self, fields):
        """Get published month."""
        values = fields.get_values("264", subfield_notation="c")
        return "".join(values)

    def get_description(self, fields):
        """Get descriptions."""
        descriptions = fields.get_subfields("300", subfield_notations=["a", "b"])

        out = []
        for desc in descriptions:
            for _, val in desc.items():
                out.append(", ".join(val))

        return ", ".join(out)

    def get_resource_type(self, fields):
        """Get resource type."""
        resource_type = fields.get_values("970", "2", "_", subfield_notation="d")
        resource_types = {
            ResourceTypeEnum.HSMASTER.value: _("Masterthesis"),
            ResourceTypeEnum.HSDISS.value: _("Dissertation"),
        }

        if not resource_type:
            return ""
        if resource_type[0] in resource_types.keys():
            return resource_types.get(resource_type[0])

        return resource_type[0]
