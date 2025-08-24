// This file is part of Invenio.
//
// Copyright (C) 2024-2025 Graz University of Technology.
//
// Invenio-Catalogue-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import React from "react";
import ReactDOM from "react-dom";

import { getInputFromDOM } from "@js/invenio_rdm_records";

import { CatalogueDepositForm } from "./CatalogueDepositForm";

const depositContainerDiv = document.getElementById("marc21-catalogue-deposit-page");

if (depositContainerDiv) {
  ReactDOM.render(
    <CatalogueDepositForm
      record={getInputFromDOM("marc21-catalogue-deposit-record")}
      files={getInputFromDOM("marc21-catalogue-deposit-files")}
      config={getInputFromDOM("marc21-catalogue-deposit-config")}
      templates={getInputFromDOM("marc21-catalogue-deposit-templates")}
      permissions={getInputFromDOM("marc21-catalogue-deposit-permissions")}
    />,
    depositContainerDiv
  );
}
