# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 UI record response serializers."""


from invenio_records_marc21.resources.serializers.ui import Marc21UIJSONSerializer

from .schema import Marc21CatalogueDepositSchema


class Marc21CatalogueDepositSerializer(Marc21UIJSONSerializer):
    """UI JSON serializer implementation."""

    def __init__(
        self, object_schema_cls=Marc21CatalogueDepositSchema, object_key="ui", **options
    ):
        """Marc21 UI JSON Constructor.

        :param object_schema_cls: object schema serializing the Marc21 record. (default: `Marc21Schema`)
        :param object_key: str key dump ui specific information
        """
        super().__init__(
            object_schema_cls=object_schema_cls, object_key=object_key, **options
        )
