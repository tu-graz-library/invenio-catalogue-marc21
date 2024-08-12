# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Catalogue service component for ."""


from .config import (
    Marc21DraftFilesResourceConfig,
    Marc21ParentRecordLinksResourceConfig,
    Marc21RecordFilesResourceConfig,
    Marc21RecordResourceConfig,
)
from .resources import Marc21ParentRecordLinksResource, Marc21RecordResource

__all__ = (
    "Marc21RecordResource",
    "Marc21DraftFilesResourceConfig",
    "Marc21RecordFilesResourceConfig",
    "Marc21RecordResourceConfig",
    "Marc21ParentRecordLinksResourceConfig",
    "Marc21ParentRecordLinksResource",
)
