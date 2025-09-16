import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

interface LogEntry {
  type: string;
  message?: {
    role: string;
    content: any[];
    usage?: {
      input_tokens: number;
      cache_creation_input_tokens: number;
      cache_read_input_tokens: number;
      output_tokens: number;
    };
    model?: string;
  };
}

async function processLine(line: string, lineNumber: number, seenMessageIds: Set<string>): { toolUses: number, cacheTokens: number } {
  if (!line.trim()) return { toolUses: 0, cacheTokens: 0 };

  try {
    const entry: LogEntry = JSON.parse(line);

    // Count tool calls
    let toolUses = 0;
    if (entry.type === 'assistant' && entry.message?.content) {
      toolUses = entry.message.content.filter((c: any) => c.type === 'tool_use').length;
    }

    // Get cache creation tokens
    const cacheTokens = entry.message?.usage?.cache_creation_input_tokens || 0;

    let description = entry.type;
    if (entry.type === 'assistant' && entry.message?.content) {
      // Get tool names if there are tool_use entries
      const toolNames = entry.message.content
        .filter((c: any) => c.type === 'tool_use')
        .map((c: any) => c.name || 'unknown')
        .join(', ');

      // Get text content if present
      const textContent = entry.message.content
        .filter((c: any) => c.type === 'text')
        .map((c: any) => c.text || '')
        .join(' ')
        .trim();

      if (toolNames) {
        description = `assistant (tool: ${toolNames})`;
      } else if (textContent) {
        const preview = textContent.substring(0, 10);
        description = `assistant ("${preview}${textContent.length > 10 ? '...' : ''}")`;
      } else {
        const types = entry.message.content.map((c: any) => c.type).join(', ');
        description = `assistant (${types})`;
      }

      // Check if this is a continuation message (same id)
      const messageId = (entry.message as any).id;
      if (messageId && seenMessageIds.has(messageId)) {
        // Skip printing continuation messages
        return { toolUses, cacheTokens: 0 };  // Don't double-count cache tokens
      } else if (messageId) {
        seenMessageIds.add(messageId);
      }
    } else if (entry.type === 'user' && entry.message?.content) {
      const types = entry.message.content.map((c: any) => c.type).join(', ');
      description = `user (${types})`;
    } else if (entry.type === 'result') {
      const result = (entry as any).result;
      if (result) {
        const preview = result.substring(0, 20);
        description = `result: "${preview}${result.length > 20 ? '...' : ''}"`;
      }
    }

    // Only print if there are cache tokens or it's an important line
    if (cacheTokens > 0 || entry.type === 'assistant' || entry.type === 'result') {
      console.log(`Line ${lineNumber}: ${description.padEnd(40)} cache_creation: ${cacheTokens}`);
    }

    return { toolUses, cacheTokens };

  } catch (e) {
    // Skip parse errors silently
    return { toolUses: 0, cacheTokens: 0 };
  }
}

async function streamFromStdin() {
  let toolCallCount = 0;
  let totalCacheTokens = 0;
  let lineNumber = 0;
  let seenMessageIds = new Set<string>();

  console.log('Streaming cache_creation_input_tokens:');
  console.log('-'.repeat(50));

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
  });

  for await (const line of rl) {
    lineNumber++;
    const result = await processLine(line, lineNumber, seenMessageIds);
    toolCallCount += result.toolUses;
    totalCacheTokens += result.cacheTokens;
  }

  console.log('-'.repeat(50));
  console.log(`\nTotal tool calls: ${toolCallCount}`);
  console.log(`Total cache creation tokens: ${totalCacheTokens}`);
}

async function processLines(lines: string[]) {
  let toolCallCount = 0;
  let totalCacheTokens = 0;
  let lineNumber = 0;
  let seenMessageIds = new Set<string>();

  console.log('Line-by-line cache_creation_input_tokens:');
  console.log('-'.repeat(50));

  for (const line of lines) {
    lineNumber++;
    const result = await processLine(line, lineNumber, seenMessageIds);
    toolCallCount += result.toolUses;
    totalCacheTokens += result.cacheTokens;
  }

  console.log('-'.repeat(50));
  console.log(`\nTotal tool calls: ${toolCallCount}`);
  console.log(`Total cache creation tokens: ${totalCacheTokens}`);
}

async function inspectFile(filePath: string) {
  const content = await fs.readFile(filePath, 'utf-8');
  const lines = content.trim().split('\n');
  await processLines(lines);
}

// Main
async function main() {
  const isStdin = process.argv.includes('--stdin') || process.argv.includes('-');

  if (isStdin) {
    await streamFromStdin();
  } else {
    const filePath = process.argv[2] || path.join(__dirname, '..', 'logs', 'claude_output.jsonl');
    await inspectFile(filePath);
  }
}

main().catch(console.error);