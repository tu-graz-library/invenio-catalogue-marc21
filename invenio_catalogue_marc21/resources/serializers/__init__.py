# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2025 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 Resources serializers module."""

from .base import CatalogueSchema
from .deposit import Marc21CatalogueDepositSerializer
from .ui import Marc21CatalogueUIJSONSerializer

__all__ = (
    "Marc21CatalogueDepositSerializer",
    "CatalogueSchema",
    "Marc21CatalogueUIJSONSerializer",
)
