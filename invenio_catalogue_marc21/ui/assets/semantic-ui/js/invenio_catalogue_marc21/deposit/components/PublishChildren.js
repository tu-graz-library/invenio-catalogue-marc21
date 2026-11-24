/*
 * SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import axios from "axios";
import PropTypes from "prop-types";
import React, { PureComponent, useState } from "react";
import { connect } from "react-redux";
import {
  Button,
  Divider,
  Icon,
  Label,
  List,
  Loader,
  Modal,
  ModalActions,
  ModalContent,
  ModalHeader,
} from "semantic-ui-react";

const api = axios.create({
  withCredentials: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
  headers: { Accept: "application/json" },
});

const gap = { marginLeft: "0.75em" };

function CheckItem({ title, checked, status, onToggle }) {
  return (
    <List.Item>
      <Icon
        link
        size="large"
        name={checked ? "check square" : "square outline"}
        color={checked ? "green" : "grey"}
        onClick={onToggle}
      />
      <List.Content verticalAlign="middle">
        {title}
        {status?.state === "pending" && (
          <Loader active inline size="mini" style={gap} />
        )}
        {status?.state === "success" && (
          <Label basic color="green" size="mini" style={gap}>
            <Icon name="check" /> published
          </Label>
        )}
        {status?.state === "error" && (
          <Label basic color="red" size="mini" style={gap}>
            <Icon name="warning circle" /> {status.error || "Unknown error"}
          </Label>
        )}
      </List.Content>
    </List.Item>
  );
}

function CheckList({ items, checked, statuses, onToggle, onSelectAll, onClear }) {
  return (
    <>
      <Button.Group size="mini" compact>
        <Button
          icon="circle"
          content="Select all"
          disabled={checked.size === items.length}
          onClick={onSelectAll}
        />
        <Button
          icon="circle outline"
          content="Clear"
          disabled={checked.size === 0}
          onClick={onClear}
        />
      </Button.Group>
      <Divider />
      <List relaxed>
        {items.map(({ pid, title }) => (
          <CheckItem
            key={pid}
            title={title}
            checked={checked.has(pid)}
            status={statuses[pid]}
            onToggle={() => onToggle(pid)}
          />
        ))}
      </List>
    </>
  );
}

function PublishChildrenCmp({ children: items = [] }) {
  const [open, setOpen] = useState(false);
  const [checked, setChecked] = useState(new Set()); // pids of checked items
  const [statuses, setStatuses] = useState({}); // pid -> { state, error? }

  const publishing = Object.values(statuses).some((s) => s.state === "pending");

  const handleOpen = () => {
    setChecked(new Set());
    setStatuses({});
    setOpen(true);
  };

  const handleClose = () => setOpen(false);

  const toggle = (pid) => {
    const next = new Set(checked);
    next.has(pid) ? next.delete(pid) : next.add(pid);
    setChecked(next);
  };

  const selectAll = () => {
    setChecked(new Set(items.map((i) => i.pid)));
  };

  const clear = () => {
    setChecked(new Set());
  };

  const setStatus = (pid, status) => {
    setStatuses((prev) => ({ ...prev, [pid]: status }));
  };

  const publishOne = async ({ pid }) => {
    setStatus(pid, { state: "pending" });
    try {
      const { data } = await api.post(`/api/catalogue/${pid}/draft/actions/publish`);
      setStatus(
        pid,
        data.success ? { state: "success" } : { state: "error", error: data.error }
      );
    } catch (error) {
      setStatus(pid, {
        state: "error",
        error: error.response?.data?.error || error.message,
      });
    }
  };

  // publishes all checked items that have not succeeded yet
  const publish = () => {
    items
      .filter((i) => checked.has(i.pid) && statuses[i.pid]?.state !== "success")
      .forEach(publishOne);
  };

  return (
    <>
      <Button
        compact
        fluid
        onClick={handleOpen}
        icon="file"
        labelPosition="left"
        content="Publish Children"
      />
      <Modal size="large" open={open} onClose={handleClose}>
        <ModalHeader>Publish Children</ModalHeader>
        <ModalContent>
          <CheckList
            items={items}
            checked={checked}
            statuses={statuses}
            onToggle={toggle}
            onSelectAll={selectAll}
            onClear={clear}
          />
        </ModalContent>
        <ModalActions>
          <Button negative disabled={publishing} onClick={handleClose}>
            Close
          </Button>
          <Button
            positive
            loading={publishing}
            disabled={publishing || checked.size === 0}
            onClick={publish}
          >
            Publish
          </Button>
        </ModalActions>
      </Modal>
    </>
  );
}

const mapStateToProps = null;

const mapDispatchToProps = (dispatch) => ({});

export const PublishChildren = connect(
  mapStateToProps,
  mapDispatchToProps
)(PublishChildrenCmp);
