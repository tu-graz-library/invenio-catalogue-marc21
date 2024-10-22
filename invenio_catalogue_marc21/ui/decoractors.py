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
