# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module link multiple marc21 modules."""


def init(app):
    """Init app."""
    # Register services - cannot be done in extension because
    # Invenio-Records-Resources might not have been initialized.

    ext = app.extensions["invenio-catalogue-marc21"]
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(ext.records_service, service_id="marc21-catalogue-records")
    sregistry.register(ext.records_service.files, service_id="marc21-catalogue-files")
    sregistry.register(
        ext.records_service.draft_files, service_id="marc21-catalogue-draft-files"
    )

    # iregistry = app.extensions["invenio-indexer"].registry
    # iregistry.register(ext.records_service.indexer, indexer_id="marc21-records")
    # iregistry.register(
    #     ext.records_service.draft_indexer, indexer_id="marc21-records-drafts"
    # )


def create_record_bp(app):
    """Create records blueprint."""
    ext = app.extensions["invenio-catalogue-marc21"]
    return ext.record_resource.as_blueprint()


def create_catalogue_bp(app):
    """Create records blueprint."""
    ext = app.extensions["invenio-catalogue-marc21"]
    return ext.record_catalgoue.as_blueprint()