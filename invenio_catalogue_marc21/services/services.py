# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module link multiple marc21 modules."""


from invenio_db import db
from invenio_records_marc21.services import Marc21RecordFilesService, Marc21Metadata
from invenio_records_resources.services.uow import unit_of_work


class Marc21CatalogueService(Marc21RecordFilesService):
    """Marc21 record service class."""

    def _create_data(
        self, identity, data=None, metadata=None, files=False, access=None
    ):
        """Create a data json.

        :param identity: Identity of user creating the record.
        :type identity: `flask_principal.identity`
        :param data: Input data according to the data schema.
        :type data: dict
        :param metadata: Input data according to the metadata schema.
        :type metadata: `services.record.Marc21Metadata`
        :param files: enable/disable file support for the record.
        :type files: bool
        :param dict access: provide access additional information
        :return: marc21 record dict
        :rtype: dict
        """
        if data is None:
            data = metadata.json
        if "files" not in data:
            data["files"] = {"enabled": files}
        if "access" not in data:
            default_access = {
                "access": {
                    "record": "public",
                    "files": "public",
                },
            }
            if access is not None:
                default_access["access"].update(access)
            data.update(default_access)
        return data

    @unit_of_work()
    def create(
        self,
        identity,
        data=None,
        metadata=Marc21Metadata(),
        files=False,
        access=None,
        uow=None,
    ):
        """Create a draft record.

        :param identity: Identity of user creating the record.
        :type identity: `flask_principal.identity`
        :param data: Input data according to the data schema.
        :type data: dict
        :param metadata: Input data according to the metadata schema.
        :type metadata: `services.record.Marc21Metadata`
        :param files: enable/disable file support for the record.
        :type files: bool
        :param dict access: provide access additional information
        :return: marc21 record item
        :rtype: `invenio_records_resources.services.records.results.RecordItem`
        """
        data = self._create_data(identity, data, metadata, files, access)
        return super().create(identity=identity, data=data)

    @unit_of_work()
    def update_draft(
        self,
        identity,
        id_,
        data=None,
        metadata=Marc21Metadata(),
        revision_id=None,
        access=None,
        uow=None,
    ):
        """Update a draft record.

        :param identity: Identity of user creating the record.
        :type identity: `flask_principal.identity`
        :param data: Input data according to the data schema.
        :type data: dict
        :param metadata: Input data according to the metadata schema.
        :type metadata: `services.record.Marc21Metadata`
        :param files: enable/disable file support for the record.
        :type files: bool
        :param dict access: provide access additional information
        :return: marc21 record item
        :rtype: `invenio_records_resources.services.records.results.RecordItem`
        """
        data = self._create_data(identity, data, metadata, access=access)
        return super().update_draft(
            identity=identity, id_=id_, data=data, revision_id=revision_id
        )
