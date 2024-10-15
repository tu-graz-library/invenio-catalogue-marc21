# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 UI record response serializers."""


from copy import deepcopy
from datetime import datetime

from flask_resources.serializers import JSONSerializer
from invenio_records_marc21.resources.serializers.ui import (
    Marc21UIJSONSerializer,
    Marc21UIXMLSerializer,
)
from lxml import etree

from ..schema import Marc21Schema
from .schema import Marc21CatalogueUISchema


class Marc21CatalogueUIJSONSerializer(Marc21UIJSONSerializer):
    """Marc21 JSON export serializer implementation."""

    def __init__(
        self,
        format_serializer_cls=JSONSerializer,
        object_schema_cls=Marc21CatalogueUISchema,
        **options
    ):
        """Marc21 Base Serializer Constructor.

        :param schema_cls: Default Marc21Schema
        :param options: Json encoding options.
        """
        super().__init__(
            format_serializer_cls=format_serializer_cls,
            object_schema_cls=object_schema_cls,
            **options
        )


class Marc21CatalogueUIXMLSerializer(Marc21UIXMLSerializer):
    """UI Marc21 xml serializer implementation."""

    def __init__(
        self,
        format_serializer_cls=JSONSerializer,
        object_schema_cls=Marc21CatalogueUISchema,
        **options
    ):
        """Marc21 Base Serializer Constructor.

        :param schema_cls: Default Marc21Schema
        :param options: Json encoding options.
        """
        super().__init__(
            format_serializer_cls=format_serializer_cls,
            object_schema_cls=object_schema_cls,
            **options
        )
