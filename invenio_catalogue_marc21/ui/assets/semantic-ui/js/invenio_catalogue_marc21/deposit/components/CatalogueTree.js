// This file is part of Invenio.
//
// Copyright (C) 2024-2025 Graz University of Technology.
//
// Invenio-Catalogue-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import PropTypes from "prop-types";
import React from "react";
import { Card } from "semantic-ui-react";

import { Tree } from "./Tree";

export const CatalogueTree = ({ catalogue }) => {
  return (
    <Card className="catalogue-field" fluid>
      <Card.Content>
        <Tree data={catalogue} />
      </Card.Content>
    </Card>
  );
};

CatalogueTree.propTypes = {
  catalogue: PropTypes.object.isRequired,
};
