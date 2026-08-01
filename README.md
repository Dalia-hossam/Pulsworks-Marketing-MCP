# PulseWorks Marketing MCP Server

## Project Overview

This project implements a Model Context Protocol (MCP) Server for PulseWorks Marketing.

The goal is to provide a secure, standardized interface between an AI assistant and the company's marketing database without exposing direct database access.

The MCP Server allows the AI assistant to retrieve campaign information, access company performance metrics, generate analytical reports, and execute authorized marketing actions while enforcing strict validation and role-based access control (RBAC).

---

## Problem Statement

Marketing employees need fast, natural language access to campaign performance and customer data. 

Allowing an LLM to connect directly to an enterprise database is unsafe because it may:

- Access unauthorized or sensitive financial data
- Perform unauthorized database mutations or deletions
- Bypass corporate security policies
- Execute invalid or malformed SQL queries

The MCP Server solves this by acting as a secure, sandboxed mediation layer between the AI model and the underlying database.

---

## Technologies

- **Python 3.12+**
- **SQLite3** (Relational Database with SQL Seeding)
- **MCP Python SDK** (`mcp`)
- **FastMCP & Pydantic** (Schema Validation)
- **Asyncio & Stdio Transport Protocol**
- **Git & GitHub**

---

## Project Structure

```text
Pulsworks-Marketing-MCP/

client/
├── agent.py          # Interactive Local MCP Client / Agent
└── demo.py           # Comprehensive evaluation suite for MCP protocol concerns

db/
├── schema.sql        # Database schema definitions
└── seed.sql          # Initial mock data (users, campaigns, results)

docs/                 # System documentation & specifications

mcp_server/
├── auth.py           # Authentication & RBAC security enforcement layer
├── database.py       # SQLite connection manager & query layer
└── server.py         # Primary MCP Server implementation & tool definitions

requirements.txt      # Python package dependencies
README.md             # Project documentation

## Current Features

- SQLite Database
- Authentication
- Role-based Authorization
- MCP Tool Suite
- Input Validation
-Resources & System Prompts
- Interactive Offline MCP Agent
- Full Verification Suite

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
```

## Authors

**Name:** Dalia Hossam

Alexandria University

Data Science Student
