# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module link multiple marc21 modules."""

from flask import Flask
from invenio_i18n import gettext as _
from invenio_rdm_records.services.pids import PIDManager, PIDsService
from invenio_records_marc21.services import (
    Marc21DraftFilesServiceConfig,
    Marc21RecordFilesServiceConfig,
)
from invenio_records_resources.services import FileService

from . import config
from .resources import (
    Marc21CatalogueRecordResource,
    Marc21CatalogueRecordResourceConfig,
)
from .services import Marc21CatalogueService, Marc21CatalogueServiceConfig
from .views import init


class InvenioCatalogueMarc21(object):
    """invenio-catalogue-marc21 extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        # TODO: This is an example of translation string with comment. Please
        # remove it.
        # NOTE: This is a note to a translator.
        _("A translation string")
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_services(app)
        self.init_resources(app)
        app.extensions["invenio-catalogue-marc21"] = self

    def init_config(self, app):
        """Initialize configuration."""
        # Use theme's base template if theme is installed
        for k in dir(config):
            if k.startswith("MARC21_CATALOGUE_"):
                app.config.setdefault(k, getattr(config, k))

    def service_configs(self, app):
        """Customized service configs."""

        class ServiceConfigs:
            record = Marc21CatalogueServiceConfig.build(app)
            file = Marc21RecordFilesServiceConfig.build(app)
            file_draft = Marc21DraftFilesServiceConfig.build(app)

        return ServiceConfigs

    def init_services(self, app):
        """Initialize services."""
        service_config = self.service_configs(app)

        self.records_service = Marc21CatalogueService(
            config=service_config.record,
            files_service=FileService(service_config.file),
            draft_files_service=FileService(service_config.file_draft),
            pids_service=PIDsService(service_config.record, PIDManager),
        )

    def init_resources(self, app):
        """Initialize resources."""
        self.record_resource = Marc21CatalogueRecordResource(
            service=self.records_service,
            config=Marc21CatalogueRecordResourceConfig,
        )
        pass


def finalize_app(app: Flask) -> None:
    """Finalize app."""
    init(app)


def api_finalize_app(app: Flask) -> None:
    """Finalize app for api."""
    init(app)
