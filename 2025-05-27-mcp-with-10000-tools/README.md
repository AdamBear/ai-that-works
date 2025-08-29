
# 🦄 12-factor agents: selecting from thousands of MCP tools

> MCP is only as great as your ability to pick the right tools. We'll dive into showing how to leverage MCP servers and accurately use the right ones when only a few have actually relevant tools.

[Video](https://www.youtube.com/watch?v=P5wRLKF4bt8)

[![12-factor agents: selecting from thousands of MCP tools](https://img.youtube.com/vi/P5wRLKF4bt8/0.jpg)](https://www.youtube.com/watch?v=P5wRLKF4bt8)

## Overview

This session explores how to efficiently select and use the right tools from thousands of available MCP (Model Context Protocol) tools. We'll cover strategies for tool discovery, selection, and integration in production AI agents.

## Key Topics

- MCP server architecture and tool discovery
- Strategies for tool selection from large tool sets
- Building efficient tool routing systems
- Managing tool dependencies and conflicts
- Performance considerations with many tools

## Running this code

### Installing dependencies

```bash
# Install dependencies
uv sync
```

### Generate BAML code

```bash
# Convert BAML files -> Python
uv run baml-cli generate
```

### Run the code

```bash
# Run the tool selection system
python tools.py
```

## Key Files

- `tools.json` - Contains metadata for 10,674 tools from 1,285 MCP servers
- `tools.py` - Main tool selection and routing logic
- `parse_json_schema.py` - Utilities for parsing tool schemas
- `baml_src/` - BAML configuration for LLM interactions

## Resources

- [Session Recording](https://www.youtube.com/watch?v=P5wRLKF4bt8)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [Discord Community](https://boundaryml.com/discord)
- Sign up for the next session on [Luma](https://lu.ma/baml)