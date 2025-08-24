# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2025 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module link multiple marc21 modules."""


from .config import Marc21CatalogueServiceConfig, Marc21CatalogueTasksServiceConfig
from .services import Marc21CatalogueService, Marc21CatalogueTasksService

__all__ = (
    "Marc21CatalogueService",
    "Marc21CatalogueServiceConfig",
    "Marc21CatalogueTasksService",
    "Marc21CatalogueTasksServiceConfig",
)
