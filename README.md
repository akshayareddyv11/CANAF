# CANAF - Compliance Aware Network Automation Framework

CANAF is a network automation project that validates Cisco IOS-XE device configurations against compliance policies before deployment.

## Problem Statement

Network automation can push configurations quickly, but fast deployment without compliance checks can also push insecure changes at scale.

CANAF solves this by adding a policy-as-code compliance gate before deployment.

## Features

- Connects to Cisco IOS-XE devices using Netmiko
- Collects running configurations automatically
- Validates configurations using YAML policy files
- Generates JSON compliance reports
- Blocks deployment if compliance checks fail
- Deploys compliant configurations using Ansible
- Displays compliance status using a Flask dashboard

## Workflow

```text
Cisco IOS-XE Device
        ↓
Netmiko collects running config
        ↓
Python compliance checker
        ↓
YAML policy-as-code rules
        ↓
JSON compliance report
        ↓
Deployment gate
        ↓
PASS → Ansible deploy
FAIL → Block deployment
        ↓
Flask dashboard

- project structure 

CANAF/
├── ansible/
│   ├── inventory/
│   └── playbooks/
├── compliance/
│   ├── policies/
│   ├── reports/
│   ├── checker.py
│   └── device_connection.py
├── dashboard/
│   └── app.py
├── deploy.py
├── requirements.txt
└── README.md
