// This file is part of Invenio.
//
// Copyright (C) 2024-2025 Graz University of Technology.
//
// Invenio-Catalogue-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React, { Component } from "react";
import Overridable from "react-overridable";
import { Card, Divider, Grid } from "semantic-ui-react";

import { DeleteButton, PublishButton, SaveButton } from "@js/invenio_rdm_records";
import {
  FilesAccess,
  MetadataAccess,
} from "@js/invenio_rdm_records/src/deposit/fields/AccessField/components";
import { TemplateField } from "@js/invenio_records_marc21/components";
import { i18next } from "@translations/invenio_catalogue_marc21/i18next";

//import { ImportFromAlma } from "./ImportFromAlma";
import { UploadFiles } from "./UploadFiles";

export class ManageRecord extends Component {
  constructor(props) {
    super(props);
  }

  state = {};

  render() {
    const { record, permissions, templates, config } = this.props;

    return (
      <Card>
        <Card.Content>
          <Grid relaxed>
            <Grid.Column width={16}>
              <SaveButton fluid />
              <PublishButton fluid />

              {permissions.can_delete_draft && (
                <DeleteButton
                  fluid
                  // TODO: make is_published part of the API response
                  //       so we don't have to do this
                  isPublished={record.is_published}
                />
              )}

              {templates.length > 0 && (
                <TemplateField
                  label={i18next.t("Templates")}
                  labelIcon="bookmark"
                  templates={templates}
                />
              )}

              {permissions.showMetadataAccess && (
                <>
                  <MetadataAccess record={record} />
                  <Divider hidden />
                </>
              )}

              {permissions.showFileAccess && (
                <>
                  <FilesAccess />
                  <Divider hidden />
                </>
              )}

              {permissions.showFileUploader && (
                <UploadFiles record={record} config={config} />
              )}

              {/* {permissions.showImportFromAlma && <ImportFromAlma />} */}

              <Overridable
                id="InvenioCatalogueMarc21.Manage.Container"
                record={record}
                config={config}
              >
                <></>
              </Overridable>
            </Grid.Column>
          </Grid>
        </Card.Content>
      </Card>
    );
  }
}
