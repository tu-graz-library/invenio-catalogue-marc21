# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Catalogue service component for ."""


from flask import g
from flask_resources import resource_requestctx, response_handler, route
from invenio_drafts_resources.resources import RecordResource
from invenio_records_marc21.services.record.metadata import Marc21Metadata
from invenio_records_resources.resources.records.resource import (
    request_data,
    request_extra_args,
    request_headers,
    request_search_args,
    request_view_args,
)
from invenio_records_resources.resources.records.utils import search_preference

from . import config


#
# Records
#
class Marc21CatalogueRecordResource(RecordResource):
    """Bibliographic record resource."""

    config_name = "MARC21_RECORDS_RECORD_CONFIG"
    default_config = config.Marc21CatalogueRecordResourceConfig

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes

        def s(route):
            """Suffix a route with the URL prefix."""
            return f"{route}{self.config.url_prefix}"

        def p(route):
            """Prefix a route with the URL prefix."""
            return f"{self.config.url_prefix}{route}"

        rules = [
            # route("GET", p(routes["list"]), self.search),
            route("POST", p(routes["list"]), self.create),
            route("GET", p(routes["item"]), self.read),
            route("PUT", p(routes["item"]), self.update),
            route("DELETE", p(routes["item"]), self.delete),
            route("POST", p(routes["item-draft"]), self.edit),
            route("PUT", p(routes["item-draft"]), self.update_draft),
            route("DELETE", p(routes["item-draft"]), self.delete_draft),
            route("POST", p(routes["item-publish"]), self.publish),
            # Additional routes
            # route("GET", p(routes["item-tree"]), self.tree),
        ]
        return rules

    def convert_record(self, data):
        """Convert metadata to a dict."""
        metadata = Marc21Metadata()
        metadata.xml = data["metadata"]
        data["metadata"] = metadata.json.get("metadata", {})
        return data

    @request_data
    @response_handler()
    def create(self):
        """Create an item.

        POST /catalogue/
        """

        data = resource_requestctx.data
        data = self.convert_record(data)
        item = self.service.create(
            g.identity,
            data=data,
        )
        return item.to_dict(), 201

    @request_headers
    @request_view_args
    @request_data
    @response_handler()
    def update_draft(self):
        """Update a draft.

        PUT /catalogue/:pid_value/draft
        """
        data = resource_requestctx.data
        data = self.convert_record(data)
        item = self.service.update_draft(
            g.identity,
            resource_requestctx.view_args["pid_value"],
            data,
            revision_id=resource_requestctx.headers.get("if_match"),
        )
        return item.to_dict(), 200

    #
    @request_extra_args
    @request_search_args
    @response_handler(many=True)
    def tree(self):
        """Perform a search over the items."""
        identity = g.identity
        pid_value = resource_requestctx.view_args["pid_value"]
        hits = self.service.search(
            identity=identity,
            params=resource_requestctx.args,
            search_preference=search_preference(),
            expand=resource_requestctx.args.get("expand", False),
        )
        return hits.to_dict(), 200
