# 第 1 章 - CLI 和代理循环

现在让我们添加 BAML 并创建我们的第一个带有 CLI 接口的代理。

首先，我们需要安装 [BAML](https://github.com/boundaryml/baml)
这是一个用于提示和结构化输出的工具。

如果您使用 cursor 或 VSCode，您可能还想安装 VSCode 的 BAML 扩展。但是，如果您使用不同的编辑器或不想安装扩展，您仍然可以完成工作坊。

    npm i @boundaryml/baml

初始化 BAML

    npx baml-cli init

删除默认 resume.baml

    rm baml_src/resume.baml

添加我们的启动代理，一个单一的 BAML 提示，我们将在其上构建

    cp ./walkthrough/01-agent.baml baml_src/agent.baml

<details>
<summary>显示文件</summary>

```rust
// ./walkthrough/01-agent.baml
class DoneForNow {
  intent "done_for_now"
  message string
}

function DetermineNextStep(
    thread: string
) -> DoneForNow {
    client "openai/gpt-4o"

    prompt #"
        {{ _.role("system") }}

        You are a helpful assistant that can help with tasks.

        {{ _.role("user") }}

        You are working on the following thread:

        {{ thread }}

        What should the next step be?

        {{ ctx.output_format }}
    "#
}

test HelloWorld {
  functions [DetermineNextStep]
  args {
    thread #"
      {
        "type": "user_input",
        "data": "hello!"
      }
    "#
  }
}
```

</details>

生成 BAML 客户端代码

    npx baml-cli generate

为开发启用 BAML 日志

    export BAML_LOG=debug

添加 CLI 接口

    cp ./walkthrough/01-cli.ts src/cli.ts

<details>
<summary>显示文件</summary>

```ts
// ./walkthrough/01-cli.ts
// cli.ts 允许您从命令行调用代理循环

import { agentLoop, Thread, Event } from "./agent";

export async function cli() {
    // 获取命令行参数，跳过前两个 (node 和脚本名称)
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.error("Error: Please provide a message as a command line argument");
        process.exit(1);
    }

    // 将所有参数连接成单个消息
    const message = args.join(" ");

    // 使用用户消息作为初始事件创建新线程
    const thread = new Thread([{ type: "user_input", data: message }]);

    // 使用线程运行代理循环
    const result = await agentLoop(thread);
    console.log(result);
}
```

</details>

更新 index.ts 以使用 CLI

```diff
src/index.ts
+import { cli } from "./cli"

 async function hello(): Promise<void> {
     console.log('hello, world!')

 async function main() {
-    await hello()
+    await cli()
 }
```

<details>
<summary>跳过此步骤</summary>

    cp ./walkthrough/01-index.ts src/index.ts

</details>

添加代理实现

    cp ./walkthrough/01-agent.ts src/agent.ts

<details>
<summary>显示文件</summary>

```ts
// ./walkthrough/01-agent.ts
import { b } from "../baml_client";

// tool call 或响应人类工具
type AgentResponse = Awaited<ReturnType<typeof b.DetermineNextStep>>;

export interface Event {
    type: string
    data: any;
}

export class Thread {
    events: Event[] = [];

    constructor(events: Event[]) {
        this.events = events;
    }

    serializeForLLM() {
        // 可以更改为任何自定义序列化，XML 等
        // e.g. https://github.com/got-agents/agents/blob/59ebbfa236fc376618f16ee08eb0f3bf7b698892/linear-assistant-ts/src/agent.ts#L66-L105
        return JSON.stringify(this.events);
    }
}

// 现在这只是运行一轮与 LLM，但
// 我们将更新此函数以处理所有代理逻辑
export async function agentLoop(thread: Thread): Promise<AgentResponse> {
    const nextStep = await b.DetermineNextStep(thread.serializeForLLM());
    return nextStep;
}
```

</details>

BAML 代码默认配置使用 OPENAI_API_KEY

在测试时，您可以将模型 / 提供商更改为其他任何东西
如您所愿

        client "openai/gpt-4o"

[有关 BAML 客户端的文档在这里](https://docs.boundaryml.com/guide/baml-basics/switching-llms)

例如，您可以配置 [gemini](https://docs.boundaryml.com/ref/llm-client-providers/google-ai-gemini)
或 [anthropic](https://docs.boundaryml.com/ref/llm-client-providers/anthropic) 作为您的模型提供商。

如果您想运行示例而不更改，您可以将 OPENAI_API_KEY 环境变量设置为任何有效的 openai 密钥。

    export OPENAI_API_KEY=...

尝试

    npx tsx src/index.ts hello

您应该看到来自模型的熟悉响应

    {
  intent: 'done_for_now',
  message: 'Hello! How can I assist you today?'
}
