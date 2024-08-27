# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Catalogue service component for ."""


import marshmallow as ma
from flask_resources import JSONDeserializer, RequestBodyParser, ResponseHandler
from invenio_drafts_resources.resources import RecordResourceConfig
from invenio_records_marc21.resources.serializers import (
    Marc21JSONSerializer,
    Marc21XMLSerializer,
)
from invenio_records_marc21.resources.serializers.ui import (
    Marc21UIJSONSerializer,
    Marc21UIXMLSerializer,
)
from invenio_records_resources.resources.records.args import SearchRequestArgsSchema

record_serializer = {
    "application/json": ResponseHandler(Marc21JSONSerializer()),
    "application/marcxml": ResponseHandler(Marc21XMLSerializer()),
    "application/vnd.inveniomarc21.v1+json": ResponseHandler(Marc21UIJSONSerializer()),
    "application/vnd.inveniomarc21.v1+marcxml": ResponseHandler(
        Marc21UIXMLSerializer()
    ),
}

url_prefix = "/catalogue"

record_ui_routes = {
    "search": "/search",
    "list": "",
    "item": "/<pid_value>",
    "item-draft": "/<pid_value>/draft",
    "item-publish": "/<pid_value>/draft/actions/publish",
}


class Marc21CatalogueRecordResourceConfig(RecordResourceConfig):
    """Marc21 Record resource configuration."""

    blueprint_name = "marc21_catalogue_records"
    url_prefix = url_prefix

    default_accept_mimetype = "application/json"

    response_handlers = record_serializer

    request_view_args = {
        "pid_value": ma.fields.Str(),
        "pid_type": ma.fields.Str(),
    }
    links_config = {}

    routes = record_ui_routes

    # Request parsing
    request_args = SearchRequestArgsSchema
    request_view_args = {"pid_value": ma.fields.Str()}
    request_headers = {"if_match": ma.fields.Int()}
    request_body_parsers = {
        "application/json": RequestBodyParser(JSONDeserializer()),
        "application/marcxml": RequestBodyParser(JSONDeserializer()),
    }

    request_view_args = {
        "pid_value": ma.fields.Str(),
        "pid_type": ma.fields.Str(),
    }
