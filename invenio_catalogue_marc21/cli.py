# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Command-line tools for demo module."""

import random
from datetime import timedelta

import arrow
import click
from flask.cli import with_appcontext
from flask_principal import Identity, RoleNeed, UserNeed
from invenio_access.permissions import (
    any_user,
    authenticated_user,
    system_identity,
    system_user_id,
)
from invenio_rdm_records.records.systemfields.access.field.record import (
    AccessStatusEnum,
)
from invenio_rdm_records.utils import get_or_create_user

from .utils import create_fake_data, create_marc21_record


def get_user_identity(user_id):
    """Get user identity."""
    identity = Identity(user_id)
    # TODO: we need to get the user roles for specific user groups and add to the identity
    identity.provides.add(any_user)
    identity.provides.add(UserNeed(user_id))
    identity.provides.add(authenticated_user)
    identity.provides.add(RoleNeed("Marc21Manager"))
    return identity


def fake_feature_date(days=365):
    """Generates a fake feature_date."""
    start_date = arrow.utcnow().datetime
    random_number_of_days = random.randrange(1, days)
    _date = start_date + timedelta(days=random_number_of_days)
    return _date.strftime("%Y-%m-%d")


def create_fake_record():
    """Create records for demo purposes in backend."""
    data = create_fake_data()
    data_access = {"files": "public", "record": "public"}
    data["access"] = data_access
    create_marc21_record(data, data_access)


@click.group()
def catalogue():
    """InvenioMarc21 records commands."""
    pass


@catalogue.command("demo")
@with_appcontext
@click.option(
    "-u",
    "--user-email",
    default="user@demo.org",
    show_default=True,
    help="User e-mail of an existing user.",
)
@click.option(
    "--number",
    "-n",
    default=10,
    show_default=True,
    type=int,
    help="Number of records will be created.",
)
@with_appcontext
def demo(user_email, number):
    """Create number of fake records for demo purposes."""
    click.secho("Creating demo records...", fg="blue")

    user = get_or_create_user(user_email)
    if user.id == system_user_id:
        identity = system_identity
    else:
        identity = get_user_identity(user.id)

    for _ in range(number):
        create_fake_record()

    click.secho("Created records!", fg="green")
