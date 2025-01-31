// This file is part of Invenio.
//
// Copyright (C) 2024 Graz University of Technology.
//
// Invenio-Catalogue-Marc21 is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see LICENSE file for more
// details.

import axios from "axios";
import React, { useState } from "react";
import { Card, Loader, Form, Header } from "semantic-ui-react";
import { connect } from "react-redux";
import { connect as connectFormik } from "formik";
import PropTypes from "prop-types";
import { FieldLabel } from "react-invenio-forms";
import Tree from 'react-d3-tree';
import { renderForeignObjectNode } from "./CatalogueTreeItem";
// TODO: import i18next from invenio_catalogue_marc21
import { i18next } from "@translations/invenio_records_marc21/i18next";


export default class CenteredTree extends React.PureComponent {
    state = {}
  
    componentDidMount() {
      const dimensions = this.treeContainer.getBoundingClientRect();
      this.setState({
        translate: {
          x: dimensions.width / 2,
          y: dimensions.height / 2
        }
      });
    }
  
    render() {
      return (
        <div style={containerStyles} ref={tc => (this.treeContainer = tc)}>
          <Tree 
            data={debugData} 
            translate={this.state.translate} 
            orientation={'vertical'}
          />
        </div>
      );
    }
  }
  
const CatalogueTreeFieldComponent = ({ label, labelIcon, fieldPath, onError, catalogue, actionState }) => {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState({});

    // catalogue default value is set in defaultProps

    const handleApiCatalogue = async () => {
        try {
            let apiConfig = {
                withCredentials: true,
                xsrfCookieName: "csrftoken",
                xsrfHeaderName: "X-CSRFToken",
                headers: { "Accept": "application/json" },
            };
            let axiosWithConfig = axios.create(apiConfig);
            const response = await axiosWithConfig.get(`/api/catalogue/${catalogue.root}/catalogue?drafts=true`);
            setData(response.data);
            setLoading(false);
        } catch (error) {
          setLoading(false);
          onError(error.response.data.message);
        }
    };
    
    if (data.root === undefined && catalogue.root && catalogue.root !== "") {
        handleApiCatalogue();
        
    }

    const foreignObjectProps = { width: "100px", height: "100px", x: 50 };


    const renderEmptyComponent = () => (
        <Card className="catalogue-field" fluid>
            <Card.Content>
                <Card.Header>
                    <FieldLabel htmlFor={fieldPath} icon={labelIcon} label={label} />
                </Card.Header>
            </Card.Content>
            <Card.Content style={{width: "100%", height: "100vh"}}>
                <Form.Button
                    primary
                    onClick={() => {
                        // Logic to add a child
                        setLoading(true);
                        actionState = "DRAFT_SAVE_STARTED";
                    }}
                >
                    {i18next.t("Add Child")}
                </Form.Button>
            </Card.Content>
        </Card>
    );


    const renderCatalogueComponent = () => (
        <Card className="catalogue-field" fluid>
            <Card.Content>
                <Card.Header>
                    <FieldLabel htmlFor={fieldPath} icon={labelIcon} label={label} />
                </Card.Header>
            </Card.Content>
            <Card.Content style={{width: "100%", height: "100vh"}}>
                {loading ? 
                    <Loader active huge inline="centered" /> : 
                    <Tree 
                        data={catalogue}
                        allowForeignObjects
                        rootNodeClassName="marc21-catalogue-root"
                        branchNodeClassName="marc21-catalogue-branch"
                        leafNodeClassName="marc21-catalogue-leaf"
                        renderCustomNodeElement={(rd3tProps) =>
                            renderForeignObjectNode({ ...rd3tProps, foreignObjectProps })
                            }
                    />
                }
            </Card.Content>
        </Card>
    );

    
    return (
        (loading ? 
            renderCatalogueComponent() : 
            (data.root === undefined || data.root === "" ? 
                renderEmptyComponent() : renderCatalogueComponent()
            )    
        )
    );
}

CatalogueTreeFieldComponent.propTypes = {
    fieldPath: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    labelIcon: PropTypes.string,
    onError: PropTypes.func.isRequired,
    catalogue: PropTypes.object.isRequired,
    actionState: PropTypes.string,
};

CatalogueTreeFieldComponent.defaultProps = {
    fieldPath: "catalogue",
    label: i18next.t("Catalogue"),
    labelIcon: "sitemap",
    catalogue: { root: "", parent: "", children: [] },
    actionState: undefined,
};



const mapStateToProps = (state) => ({
    catalogue: state.deposit.record.catalogue,
    actionState: state.deposit.actionState,
  });
  
  export const CatalogueTreeField = connect(
    mapStateToProps,
    null
  )(connectFormik(CatalogueTreeFieldComponent));