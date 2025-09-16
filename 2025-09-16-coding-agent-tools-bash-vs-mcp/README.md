




## Code Overview


#### example claude output w/ token ccounts

```
claude -p "write foo to bar.txt" \
    --allowedTools=Write,Read,Edit \
    --output-format=stream-json \
    --verbose
```

output message (trimmed, formatted)

```
{
    "input_tokens":4,
    "cache_creation_input_tokens":24841
    "cache_read_input_tokens":4802,
    "cache_creation":{
       "ephemeral_5m_input_tokens":24841,
       "ephemeral_1h_input_tokens":0
    },
    "output_tokens":129,
    "service_tier":"standard"
}



#### Claude w/ the token counter

```
claude -p "write foo to bar.txt" \
    --allowedTools=Write,Read,Edit \
    --output-format=stream-json \
    --verbose \
    | bun run src/inspect-logs.ts --stdin
```

Running it again with the cache

```
claude -p "write foo to bar.txt" \
    --allowedTools=Write,Read,Edit \
    --output-format=stream-json \
    --verbose \
    | bun run src/inspect-logs.ts --stdin
```

Running it again without the cache

```
claude -p "PLEASE write foo to bar.txt" \
    --allowedTools=Write,Read,Edit \
    --output-format=stream-json \
    --verbose \
    | bun run src/inspect-logs.ts --stdin
```

```
Streaming cache_creation_input_tokens:
--------------------------------------------------
Line 2: assistant (text)                         cache_creation: 12672
Line 5: assistant (tool_use)                     cache_creation: 184
Line 7: assistant (tool_use)                     cache_creation: 184
Line 9: assistant (text)                         cache_creation: 185
Line 10: result                                   cache_creation: 0
--------------------------------------------------

Total tool calls: 3
Total cache creation tokens: 13225
```



#### Adding MCP tools and inspecting context differences

use mcp-linear.json to add linear mcp tools

```
claude -p "write arg foo to bar.txt" \
    --allowedTools=Write,Read,Edit \
    --output-format=stream-json \
    --verbose \
    --mcp-config=mcp-linear.json \
    | bun run src/inspect-logs.ts --stdin
```

```
Streaming cache_creation_input_tokens:
--------------------------------------------------
Line 2: assistant (text)                         cache_creation: 18395
Line 5: assistant (tool_use)                     cache_creation: 171
Line 7: assistant (tool_use)                     cache_creation: 184
Line 9: assistant (text)                         cache_creation: 207
Line 10: result                                   cache_creation: 0
--------------------------------------------------

Total tool calls: 3
Total cache creation tokens: 18957
```

#### Linear CLI

```
bun run linear-cli/linear-cli.ts get-issue ENG-1709
bun run linear-cli/linear-cli.ts get-issue ENG-1709 --comments
```

```
cp CLAUDE_linear_cli.md CLAUDE.md
```

```
claude -p "write arg foo to bar.txt" \
    --allowedTools=Bash(bun run linear-cli/:*) \
    --output-format=stream-json \
    --verbose \
    | bun run src/inspect-logs.ts --stdin
```

now fetch the issue


now fetch the issue and all comments

### now fetch with mcp

```
cp CLAUDE_linear_mcp.md CLAUDE.md
```

```
claude -p "fetch issue ENG-1709" \
    --allowedTools='mcp__linear2__*' \
    --output-format=stream-json \
    --verbose \
    --mcp-config=mcp-linear.json \
    | bun run src/inspect-logs.ts --stdin
```

```
```

```
claude -p "fetch issue ENG-1709 and all comments" \
    --allowedTools=Bash(bun run linear-cli/:*) \
    --output-format=stream-json \
    --verbose \
    --mcp-config=mcp-linear.json \
    | bun run src/inspect-logs.ts --stdin
```

```
```
