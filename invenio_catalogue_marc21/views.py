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

from flask import Blueprint, render_template
from invenio_i18n import gettext as _
from flask_login import current_user, login_required
