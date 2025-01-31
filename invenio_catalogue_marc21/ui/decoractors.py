# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Marc21 decorators backend."""

from functools import wraps
from invenio_records_resources.services.errors import PermissionDeniedError
from flask import g

from ..proxies import current_catalogue_marc21_service


def pass_catalogue(f):
    """Decorate to retrieve the record or draft using the record service."""

    @wraps(f)
    def view(**kwargs):
        pid_value = kwargs.get("pid_value")

        def get_catalogue():
            """Retrieve record."""
            return current_catalogue_marc21_service.catalogue(
                id_=pid_value, identity=g.identity
            )

        catalogue = get_catalogue()
        kwargs["catalogue"] = catalogue
        return f(**kwargs)

    return view



def pass_draft(f):
    """Decorator to retrieve the draft using the record service."""

    @wraps(f)
    def view(**kwargs):
        pid_value = kwargs.get("pid_value")
        draft = current_catalogue_marc21_service.read_draft(id_=pid_value, identity=g.identity)
        kwargs["draft"] = draft
        return f(**kwargs)

    return view


def pass_draft_files(f):
    """Decorate a view to pass a draft's files using the files service."""

    @wraps(f)
    def view(**kwargs):
        try:
            pid_value = kwargs.get("pid_value")
            files = current_catalogue_marc21_service.draft_files.list_files(id_=pid_value, identity=g.identity)
            kwargs["draft_files"] = files

        except PermissionDeniedError:
            # this is handled here because we don't want a 404 on the landing
            # page when a user is allowed to read the metadata but not the
            # files
            kwargs["draft_files"] = None

        return f(**kwargs)

    return view
