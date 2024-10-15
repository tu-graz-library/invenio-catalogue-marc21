// This file is part of Invenio.
//
// Copyright (C) 2024 Graz University of Technology.
//
// Invenio-Catalogue-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.


import React, { useState } from "react";
import { Card, Divider, Form, Header } from "semantic-ui-react";
import { http } from "react-invenio-forms";
import PropTypes from "prop-types";
import { FieldLabel } from "react-invenio-forms";
import Tree from 'react-d3-tree';
import { CatalogueTreeItem } from "./CatalogueTreeItem";
// TODO: import i18next from invenio_catalogue_marc21
import { i18next } from "@translations/invenio_records_marc21/i18next";

export const CatalogueTreeField = ({ label, labelIcon, fieldPath, rootid, catalogue, onError, size }) => {
    const [loading, setLoading] = useState(false);
    size = size || "small";
    rootid = rootid;
    catalogue = catalogue;

    const handleClick = async () => {
        setLoading(true);
        try {
          await http.post(`/api/catalogue/${rootid}`);
          window.location = `/catalogue/${rootid}`;
        } catch (error) {
          setLoading(false);
          onError(error.response.data.message);
        }
    };
    const foreignObjectProps = { width: "100px", height: "100px", x: 50 };
    return (
        <Card className="catalogue-field" fluid>
            <Card.Content>
                <Card.Header>
                    <FieldLabel htmlFor={fieldPath} icon={labelIcon} label={label} />
                </Card.Header>
            </Card.Content>
            <Card.Content style={{width: "100%", height: "100vh"}}>
                <Tree 
                    data={catalogue}
                    rootNodeClassName="marc21-catalogue-root"
                    branchNodeClassName="marc21-catalogue-branch"
                    leafNodeClassName="marc21-catalogue-leaf"
                    renderCustomNodeElement={(rd3tProps) =>
                        CatalogueTreeItem({ ...rd3tProps, foreignObjectProps })
                        }
                />
            </Card.Content>
        </Card>
    );
}

CatalogueTreeField.propTypes = {
    recid: PropTypes.string.isRequired,
    onError: PropTypes.object.isRequired,
    fieldPath: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    labelIcon: PropTypes.string,
    catalogue: PropTypes.object,
};

CatalogueTreeField.defaultProps = {
    catalogue: {
        name: 'CEO',
        children: [
            {
                name: 'Foreman',
                attributes: {
                department: 'Production',
                },
            },
            {
                name: 'Foreman',
                attributes: {
                department: 'Fabrication',
                }
            },
            {
                name: 'Foreman',
                attributes: {
                    department: 'Assembly',
                },
            }
        ]
    }
};