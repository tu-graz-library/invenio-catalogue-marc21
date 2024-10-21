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
from flask_resources.serializers import JSONSerializer
from invenio_drafts_resources.resources import RecordResourceConfig
from invenio_records_resources.resources.records.args import SearchRequestArgsSchema

from .serializers import Marc21CatalogueXMLSerializer
from .serializers.ui import (
    Marc21CatalogueUIJSONSerializer,
    Marc21CatalogueUIXMLSerializer,
)
from .serializers.catalogue import Marc21CatalogueSerializer

url_prefix = "/catalogue"


class Marc21CatalogueResourceConfig(RecordResourceConfig):
    """Marc21 Record resource configuration."""

    blueprint_name = "marc21_catalogue"
    url_prefix = url_prefix

    default_accept_mimetype = "application/json"

    response_handlers = {
        "application/json": ResponseHandler(Marc21CatalogueSerializer()),
    }

    request_view_args = {
        "pid_value": ma.fields.Str(),
        "pid_type": ma.fields.Str(),
    }
    links_config = {}

    routes = {
        "list": "/chapters",
        "item": "/chapters/<pid_value>",
    }

    # Request parsing
    request_args = SearchRequestArgsSchema
    request_view_args = {"pid_value": ma.fields.Str()}
    request_headers = {"if_match": ma.fields.Int()}
    request_body_parsers = {
        "application/json": RequestBodyParser(JSONDeserializer()),
    }

    request_view_args = {
        "pid_value": ma.fields.Str(),
        "pid_type": ma.fields.Str(),
    }


class Marc21CatalogueRecordResourceConfig(RecordResourceConfig):
    """Marc21 Record resource configuration."""

    blueprint_name = "marc21_catalogue_records"
    url_prefix = url_prefix

    default_accept_mimetype = "application/json"

    response_handlers = {
        "application/json": ResponseHandler(JSONSerializer()),
        "application/marcxml": ResponseHandler(Marc21CatalogueXMLSerializer()),
        "application/vnd.inveniomarc21.v1+json": ResponseHandler(
            Marc21CatalogueUIJSONSerializer()
        ),
        "application/vnd.inveniomarc21.v1+marcxml": ResponseHandler(
            Marc21CatalogueUIXMLSerializer()
        ),
    }

    request_view_args = {
        "pid_value": ma.fields.Str(),
        "pid_type": ma.fields.Str(),
    }
    links_config = {}

    routes = {
        "search": "/search",
        "list": "",
        "item": "/<pid_value>",
        "item-tree": "/<pid_value>/tree",
        "item-draft": "/<pid_value>/draft",
        "item-publish": "/<pid_value>/draft/actions/publish",
    }

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
