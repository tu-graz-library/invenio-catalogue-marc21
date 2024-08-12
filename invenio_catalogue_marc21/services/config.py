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
from invenio_rdm_records.services.config import has_doi, is_record_and_has_doi
from invenio_records_resources.services import (
    ConditionalLink,
    pagination_links,
)

from invenio_drafts_resources.services.records.config import (
    is_draft,
    is_record,
)
from invenio_records_resources.services.base.links import Link
from invenio_records_resources.services.files.links import FileLink
from invenio_records_resources.services.records.links import RecordLink

def is_record(record, ctx):
    """Shortcut for links to determine if record is a record."""
    return not record.is_draft


class SwitchLinks:
    """Switch link."""

    def __init__(self, cond=None, if_=None):
        """Constructor."""
        self._conditions = cond
        self._templates = if_

    def should_render(self, obj, ctx):
        """Determine if the link should be rendered."""
        for condition, template in zip(self._conditions, self._templates):
            if condition(obj, ctx):
                return template.should_render(obj, ctx)

    def expand(self, obj, ctx):
        """Determine if the link should be rendered."""
        for condition, template in zip(self._conditions, self._templates):
            if condition(obj, ctx):
                return template.expand(obj, ctx)


class Marc21CatalogueServiceConfig(Marc21RecordServiceConfig):
    """Marc21 record service config."""

    # Schemas
    # schema = Marc21RecordSchema
    # schema_parent = Marc21ParentSchema

    schema_secret_link = None
    review = None
   
    links_search = pagination_links("{+api}/publications{?args*}")

    links_search_drafts = pagination_links("{+api}/user/publications{?args*}")

    links_search_versions = pagination_links(
        "{+api}/publications/{id}/versions{?args*}"
    )

    links_item = {
        "self": SwitchLinks(
            cond=[is_record, is_record],
            if_ = [
                ConditionalLink(
                    cond=is_record,
                    if_=RecordLink("{+api}/catalogue/{id}"),
                    else_=RecordLink("{+api}/catalogue/{id}/draft"),
                ),
                ConditionalLink(
                    cond=is_record,
                    if_=RecordLink("{+api}/publications/{id}"),
                    else_=RecordLink("{+api}/publications/{id}/draft"),
                ),
            ]
        ),
        "self_html": SwitchLinks(
            cond=[is_record, is_record],
            if_ = [
                ConditionalLink(
                    cond=is_record,
                    if_=RecordLink("{+ui}/catalogue/{id}"),
                    else_=RecordLink("{+ui}/catalogue/uploads/{id}"),
                ),
                ConditionalLink(
                    cond=is_record,
                    if_=RecordLink("{+ui}/publications/{id}"),
                    else_=RecordLink("{+ui}/publications/uploads/{id}"),
                ),
            ]
        ),
        "self_doi": Link(
            "{+ui}/publications/{+pid_doi}",
            when=is_record_and_has_doi,
            vars=lambda record, vars: vars.update(
                {
                    f"pid_{scheme}": pid["identifier"].split("/")[1]
                    for (scheme, pid) in record.pids.items()
                }
            ),
        ),
        "doi": Link(
            "https://doi.org/{+pid_doi}",
            when=has_doi,
            vars=lambda record, vars: vars.update(
                {
                    f"pid_{scheme}": pid["identifier"]
                    for (scheme, pid) in record.pids.items()
                }
            ),
        ),
        "files": ConditionalLink(
            cond=is_record,
            if_=RecordLink("{+api}/publications/{id}/files"),
            else_=RecordLink("{+api}/publications/{id}/draft/files"),
        ),
        "latest": SwitchLinks(
            cond=[is_record, is_record],
            if_ = [
                RecordLink("{+api}/catalogue/{id}/versions/latest"),
                RecordLink("{+api}/publications/{id}/versions/latest"),
            ]
        ),
        "latest_html": SwitchLinks(
            cond=[is_record, is_record],
            if_ = [
                RecordLink("{+ui}/catalogue/{id}/latest"),
                RecordLink("{+ui}/publications/{id}/latest"),
            ]
        ),
        "draft": RecordLink("{+api}/publications/{id}/draft", when=is_record),
        "publish": RecordLink(
            "{+api}/publications/{id}/draft/actions/publish", when=is_draft
        ),
        "versions": RecordLink("{+api}/publications/{id}/versions"),
    }
