# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Catalogue service component for ."""

from copy import copy

from invenio_drafts_resources.services.records.components import ServiceComponent
from invenio_records_resources.services.uow import TaskOp


class CatalogueComponent(ServiceComponent):
    """Service component for Catalogue."""

    def read_draft(self, identity, draft=None):
        """Update draft handler."""
        pass

    def update_draft(self, identity, data=None, record=None, errors=None):
        """Update draft handler."""
        pass

    def delete_draft(self, identity, draft=None, record=None, force=False):
        """Delete draft handler."""
        pass

    def edit(self, identity, draft=None, record=None):
        """Edit a record handler."""
        pass

    def new_version(self, identity, draft=None, record=None):
        """New version handler."""
        pass

    def publish(self, identity, draft=None, record=None):
        """Publish handler."""
        pass

    def import_files(self, identity, draft=None, record=None):
        """Import files handler."""
        pass

    def post_publish(self, identity, record=None, is_published=False):
        """Post publish handler."""
        pass
