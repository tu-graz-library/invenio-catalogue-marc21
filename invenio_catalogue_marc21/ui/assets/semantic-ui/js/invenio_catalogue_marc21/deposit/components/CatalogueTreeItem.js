// This file is part of Invenio.
//
// Copyright (C) 2024-2025 Graz University of Technology.
//
// Invenio-Catalogue-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import PropTypes from "prop-types";

export const CatalogueTreeItem = ({ nodeData = {}, nodeToggle }) => {
  return (
    <g>
      <text style={{ font: "italic 20px serif", fill: "black" }} onClick={nodeToggle}>
        {nodeData.name}
      </text>
    </g>
  );
};

export const renderCustomNode = ({ nodeDatum, toggleNode }) => (
  <CatalogueTreeItem nodeData={nodeDatum} triggerNodeToggle={toggleNode} />
);

CatalogueTreeItem.propTypes = {
  nodeData: PropTypes.object.isRequired,
  nodeToggle: PropTypes.func.isRequired,
};
