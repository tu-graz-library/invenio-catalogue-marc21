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

from flask import Blueprint, abort, current_app, render_template, request, url_for
from flask_login import current_user, login_required
from invenio_i18n import gettext as _
from invenio_records_marc21.resources.serializers.ui import Marc21UIJSONSerializer
from invenio_records_marc21.ui.records.decorators import (
    pass_record_files,
    pass_record_or_draft,
)
from invenio_stats.proxies import current_stats


@login_required
@pass_record_or_draft
@pass_record_files
def record_detail(record=None, files=None, pid_value=None, is_preview=False):
    """Record detail page (aka landing page)."""
    files_dict = None if files is None else files.to_dict()

    emitter = current_stats.get_event_emitter("marc21-record-view")
    if record is not None and emitter is not None:
        emitter(current_app, record=record._record, via_api=False)

    # emit a record view stats event
    return render_template(
        "invenio_catalogue_marc21/landing_page/record.html",
        record=Marc21UIJSONSerializer().dump_obj(record.to_dict()),
        pid=pid_value,
        files=files_dict,
        permissions=record.has_permissions_to(
            ["edit", "new_version", "manage", "update_draft", "read_files"]
        ),
        is_preview=is_preview,
        is_draft=record._record.is_draft,
    )
