# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Catalogue service component for ."""


from .config import Marc21CatalogueRecordResourceConfig, Marc21CatalogueResourceConfig
from .resources import Marc21CatalogueRecordResource, Marc21CatalogueResource

__all__ = (
    "Marc21CatalogueRecordResourceConfig",
    "Marc21CatalogueRecordResource",
    "Marc21CatalogueResourceConfig",
    "Marc21CatalogueResource",
)
