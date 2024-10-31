# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-catalogue-marc21 is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module link multiple marc21 modules."""


from invenio_db import db
from invenio_rdm_records.services.errors import RecordDeletedException
from invenio_records_marc21.services import Marc21Metadata, Marc21RecordService
from invenio_records_resources.services.uow import unit_of_work


class Marc21CatalogueMixin:
    def _catalogue(self, identity, id_, expand=False, action="read"):
        """Build a tree of linked records.



        :param identity: Identity of user creating the record.
        :param id_: Record PID value.
        :param expand: Expand the tree.
        :param include_deleted: Include deleted records.

        """
        record = self.record_cls.pid.resolve(id_)
        self.require_permission(identity, action, record=record)

        # Run components
        for component in self.components:
            if hasattr(component, "tree"):
                component.read(identity, record=record)

        return self.result_item(
            self,
            identity,
            record,
            links_tpl=self.links_item_tpl,
            expandable_fields=self.expandable_fields,
            nested_links_item=getattr(self.config, "nested_links_item", None),
            expand=expand,
        )

    def catalogue(self, identity, id_, expand=False, include_deleted=False):
        """Build a tree of linked records.



        :param identity: Identity of user creating the record.
        :param id_: Record PID value.
        :param expand: Expand the tree.
        :param include_deleted: Include deleted records.

        """

        record = self.record_cls.pid.resolve(id_)
        catalogue = record.get("catalogue", {})
        catalogue["root"] = self.read(
            identity, catalogue["root"], expand=False
        ).to_dict()
        catalogue["parent"] = self.read(
            identity, catalogue["parent"], expand=False
        ).to_dict()

        if "children" not in catalogue:
            return catalogue
        
        child_record = []
        for child in catalogue["children"]:
            child_record.append(self.read(identity, child, expand=False).to_dict())
        catalogue["children"] = child_record
        return catalogue


class Marc21CatalogueService(Marc21RecordService, Marc21CatalogueMixin):
    """Marc21 record service class."""

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

    def read(self, identity, id_, expand=False, include_deleted=False):
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
        record = self.record_cls.pid.resolve(id_)
        result = super().read(identity, id_, expand=expand)

        if not include_deleted and record.deletion_status.is_deleted:
            raise RecordDeletedException(record, result_item=result)
        if include_deleted and record.deletion_status.is_deleted:
            can_read_deleted = self.check_permission(
                identity, "read_deleted", record=record
            )

            if not can_read_deleted:
                # displays tombstone
                raise RecordDeletedException(record, result_item=result)

        return result

    def read_draft(self, identity, id_, expand=False):
        """Retrieve a draft of a record.

        If the draft has a "deleted" published record then we return 410.
        """
        result = super().read_draft(identity, id_, expand=expand)
        # check that if there is a published deleted record then return 410
        draft = result._record
        if draft.is_published:
            record = self.record_cls.pid.resolve(id_)
            if record.deletion_status.is_deleted:
                result = super().read(identity, id_, expand=expand)
                raise RecordDeletedException(record, result_item=result)

        return result
