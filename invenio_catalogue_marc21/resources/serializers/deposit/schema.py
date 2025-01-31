# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Schema for marc21 catalogue ui records."""

from functools import partial

from invenio_records_marc21.resources.serializers.deposit.schema import (
    MetadataDepositField,
)

from ..schema import Marc21CatalogueSchema


class Marc21CatalogueDepositSchema(Marc21CatalogueSchema):
    """Marc21 catalogue deposit schema."""

    class Meta:
        """Meta class to accept unknwon fields."""

        additional = (
            "access",
            "status",
            "parent",
            "links",
            "files",
            "is_published",
            "pids",
            "versions",
        )

    metadata = MetadataDepositField(attribute="metadata")
