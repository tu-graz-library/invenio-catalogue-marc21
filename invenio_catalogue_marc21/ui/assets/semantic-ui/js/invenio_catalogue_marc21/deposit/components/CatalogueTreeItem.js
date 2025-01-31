
import { Segment } from 'semantic-ui-react';
import React from 'react';

export const CatalogueTreeItem = ({ nodeData = {}, triggerNodeToggle, foreignObjectProps = {} }) => {
  return (
    <React.Fragment>
      <foreignObject {...foreignObjectProps}>
        <Segment
          raised
          padded
        >
          <h3>{nodeData.name}</h3>
          <ul style={{ listStyleType: 'none', padding: 0 }}>
            {nodeData.attributes &&
              Object.keys(nodeData.attributes).map((labelKey, i) => (
                <li key={`${labelKey}-${i}`}>
                  {labelKey}: {nodeData.attributes[labelKey]}
                </li>
              ))}
          </ul>
          {nodeData.children && nodeData.children.length > 0 && (
            <>
              {nodeData.children.map((childNode, index) => (
                <CatalogueTreeItem
                  key={index}
                  nodeData={childNode}
                  triggerNodeToggle={triggerNodeToggle}
                  foreignObjectProps={foreignObjectProps}
                />
              ))}
            </>            
          )}
        </Segment>
      </foreignObject>
    </React.Fragment>
  );
};

const renderForeignObjectNode = ({ nodeDatum, toggleNode }) => (
  <foreignObject width="200" height="100" x="-100" y="-50">
    <CatalogueTreeItem
      nodeData={nodeDatum}
      triggerNodeToggle={toggleNode}
      foreignObjectProps={{ width: 200, height: 100 }}
    />
  </foreignObject>
);