# 第 2 章 - 添加计算器工具

让我们向我们的代理添加一些计算器工具。

让我们从添加计算器工具定义开始

这些是我们要求模型返回作为代理循环中“下一步”的简单结构化输出。

    cp ./walkthrough/02-tool_calculator.baml baml_src/tool_calculator.baml

<details>
<summary>显示文件</summary>

```rust
// ./walkthrough/02-tool_calculator.baml
type CalculatorTools = AddTool | SubtractTool | MultiplyTool | DivideTool

class AddTool {
    intent "add"
    a int | float
    b int | float
}

class SubtractTool {
    intent "subtract"
    a int | float
    b int | float
}

class MultiplyTool {
    intent "multiply"
    a int | float
    b int | float
}

class DivideTool {
    intent "divide"
    a int | float
    b int | float
}
```

</details>

现在，让我们更新代理的 DetermineNextStep 方法以
将计算器工具暴露为潜在的下一步

```diff
baml_src/agent.baml
 function DetermineNextStep(
     thread: string
-) -> DoneForNow {
+) -> CalculatorTools | DoneForNow {
     client "openai/gpt-4o"

```

<details>
<summary>跳过此步骤</summary>

    cp ./walkthrough/02-agent.baml baml_src/agent.baml

</details>

生成更新的 BAML 客户端

    npx baml-cli generate

尝试计算器

    npx tsx src/index.ts 'can you add 3 and 4'

您应该看到代理调用工具

    {
  intent: 'add',
  a: 3,
  b: 4
}
