# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module link multiple marc21 modules."""

# TODO: This is an example file. Remove it if you do not need it, including
# the templates and static folders as well as the test case.

from flask import current_app, render_template
from flask_login import login_required
from invenio_i18n import gettext as _
from invenio_records_marc21.ui.records.decorators import (
    pass_record_files,
    pass_record_or_draft,
)
from invenio_records_marc21.ui.theme.decorators import pass_draft, pass_draft_files
from invenio_records_marc21.ui.theme.deposit import empty_record
from invenio_stats.proxies import current_stats

from invenio_catalogue_marc21.resources.serializers.catalogue import (
    Marc21CatalogueSerializer,
)
from invenio_catalogue_marc21.resources.serializers.ui import (
    Marc21CatalogueUIJSONSerializer,
)
from invenio_catalogue_marc21.resources.serializers.deposit import (
    Marc21CatalogueDepositSerializer,
)
from .decoractors import pass_catalogue
from .deposit import deposit_config


@login_required
@pass_record_or_draft
@pass_catalogue
@pass_record_files
def record_detail(
    record=None, files=None, pid_value=None, is_preview=False, catalogue={}
):
    """Record detail page (aka landing page)."""
    files_dict = None if files is None else files.to_dict()

    emitter = current_stats.get_event_emitter("marc21-record-view")
    if record is not None and emitter is not None:
        emitter(current_app, record=record._record, via_api=False)

    # emit a record view stats event
    return render_template(
        "invenio_catalogue_marc21/landing_page/record.html",
        record=Marc21CatalogueUIJSONSerializer().dump_obj(record.to_dict()),
        pid=pid_value,
        files=files_dict,
        permissions=record.has_permissions_to(
            ["edit", "new_version", "manage", "update_draft", "read_files"]
        ),
        catalogue=Marc21CatalogueSerializer().dump_obj(catalogue),
        is_preview=is_preview,
        is_draft=record._record.is_draft,
    )


@login_required
def deposit_create():
    """Create a new deposit page."""
    return render_template(
        "invenio_catalogue_marc21/deposit/index.html",
        record=empty_record(),
        files=dict(default_preview=None, entries=[], links={}),
        # templates=deposit_templates(),
        forms_config=deposit_config(),
    )


@login_required
@pass_draft
@pass_draft_files
def deposit_edit(draft=None, draft_files=None, pid_value=None):
    """Edit an existing deposit."""
    serializer = Marc21CatalogueDepositSerializer()
    record = serializer.dump_obj(draft.to_dict())

    return render_template(
        "invenio_records_marc21/deposit/index.html",
        forms_config=deposit_config(apiUrl=f"/api/catalogue/{pid_value}/draft"),
        record=record,
        files=draft_files.to_dict(),
        permissions=draft.has_permissions_to(["new_version"]),
    )
