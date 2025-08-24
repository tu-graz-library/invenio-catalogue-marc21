# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Test import csv."""

from csv import DictReader
from json import load
from pathlib import Path

from invenio_catalogue_marc21.services.tasks import build_data_from_csv_row


def test_import_from_csv() -> None:
    """Test import from csv."""
    parent = Path(__file__).parent
    with Path(f"{parent}/data/import.csv").open("r") as fp:
        reader = DictReader(fp)

        row = next(reader)  # consider only first
        data = build_data_from_csv_row(row)

        with Path(f"{parent}/data/expected.json").open("r") as fp_expected:
            expected = load(fp_expected)
            assert data.json == expected
