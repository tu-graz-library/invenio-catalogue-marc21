# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module tests."""

from flask import Flask

from invenio_catalogue_marc21 import InveniocatalogueMarc21


def test_version():
    """Test version import."""
    from invenio_catalogue_marc21 import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InveniocatalogueMarc21(app)
    assert "invenio-catalogue-marc21" in app.extensions

    app = Flask("testapp")
    ext = InveniocatalogueMarc21()
    assert "invenio-catalogue-marc21" not in app.extensions
    ext.init_app(app)
    assert "invenio-catalogue-marc21" in app.extensions


def test_view(base_client):
    """Test view."""
    res = base_client.get("/")
    assert res.status_code == 200
    assert "Welcome to invenio-catalogue-marc21" in str(res.data)
