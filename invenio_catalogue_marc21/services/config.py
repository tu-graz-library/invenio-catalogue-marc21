# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module link multiple marc21 modules."""

from invenio_records_marc21.services import Marc21RecordServiceConfig
from invenio_i18n import gettext as _



class Marc21CatalogueServiceConfig(Marc21RecordServiceConfig):
    """Marc21 record service config."""

    # Schemas
    # schema = Marc21RecordSchema
    # schema_parent = Marc21ParentSchema

    schema_secret_link = None
    review = None