## 纽约工作坊先决条件

此文件夹包含 2025-05-10 纽约工作坊的先决条件

### 快速版本

跳转到 `final` 并确保您可以运行 CLI

```
export OPENAI_API_KEY=...
cd final && npx tsx src/index.ts 'hello, world'
```

**注意** 这些示例使用 OpenAI - 如果您没有 OpenAI 密钥，您可以使用另一个推理提供商（如何在 01-cli-and-agent 文件夹中的文档）。在工作坊期间，将提供推理密钥。

### 完整版本

这里有三个文件夹

- [00-hello-world](./00-hello-world) - 基本 nodejs 和 typescript 设置步骤
- [01-cli-and-agent](./01-cli-and-agent) - 设置与 LLM 对话的基本 CLI 程序
- [final](./final) - 完成 `01-cli-and-agent` 中所有步骤后的预期结果

每个都是增量的，即 01-cli-and-agent 从 00 的预期“结束状态”开始

### 设置先决条件

- `cd 00-hello-world` 并跟随 readme 步骤

完成后：

- `cd 01-cli-and-agent` 并跟随 readme 步骤

完成后，您就可以了！

您可以通过将 01-cli-and-agent 的更新内容与 `final` 中的内容比较来验证您的工作
