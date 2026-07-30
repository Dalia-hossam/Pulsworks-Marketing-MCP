# PulseWorks Marketing MCP Server

## Project Overview

This project implements a Model Context Protocol (MCP) Server for PulseWorks Marketing.

The goal is to provide a secure interface between an AI assistant and the company's marketing database without exposing direct database access.

The MCP Server allows the AI assistant to retrieve campaign information, access company policies, generate reports, and perform authorized operations while enforcing validation and role-based permissions.

---

## Problem Statement

Marketing employees need quick access to campaign information.

Allowing an LLM to connect directly to the database is unsafe because it may:

- Access unauthorized data
- Perform unauthorized actions
- Bypass company policies
- Execute invalid requests

The MCP Server solves this by acting as a secure layer between the AI model and the database.

---

## Technologies

- Python
- SQLite
- MCP SDK 1.29.0
- JSON Schema
- VS Code MCP
- Git & GitHub

---

## Project Structure

```
PulseWorks-Marketing-MCP/

client/
db/
docs/
server/

README.md
requirements.txt
run.py
```

---

## Current Features

- SQLite Database
- Authentication
- Role-based Authorization
- Campaign Tools
- Input Validation
- Resources
- Prompt Templates
- MCP Client
- MCP Server

---

## Security

The server validates every request before accessing the database.

Only authorized users can execute sensitive operations.

JSON Schema validation is applied before processing tool inputs.

---

## Future Features

- Notifications
- Elicitation
- Progress Tracking
- Streamable HTTP Transport

---

## Authors

**Name:** Dalia Hossam

Alexandria University

Data Science Student