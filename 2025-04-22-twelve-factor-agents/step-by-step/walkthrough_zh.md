### 从头构建 12 因素代理模板

从裸 TS 仓库开始并逐步构建 12 因素代理的步骤。

这里不涵盖设置 package.json 或 tsconfig.json。

您可以使用 `npx tsx hack/run-walkthrough.ts -i -d` 将此演练作为交互式脚本运行。

您可以使用 `npx tsx hack/restore-walkthrough.ts NUMBER` 恢复到特定章节（结束），例如
快速转发到第 3 章结束，您可以运行

```
npx tsx hack/restore-walkthrough.ts 3
```

## 逐步演练

#### 清理

确保您从干净的状态开始

```
rm -rf baml_src/ && rm -rf src/ && mkdir src
```

```
git add . && git commit -m "clean up" && git show HEAD --color=always | cat
```

#### 第 0 章 - hello world

```
cp walkthrough/00-index.ts src/index.ts
npx tsx src/index.ts
```

```
git add . && git commit -m "hello world" && git show HEAD --color=always | cat
```

#### 第 1 章 - CLI 和代理循环

```
npm i baml
npx baml-cli init
# 清理默认文件
rm baml_src/resume.baml
```

添加我们的 BAML 启动代理

```
cp walkthrough/01-agent.baml baml_src/agent.baml
npx baml-cli generate
```

现在，让我们启用 BAML 日志

```
export BAML_LOG=debug
```

从我们的 ts 文件调用它

```
cp walkthrough/01-cli.ts src/cli.ts
cp walkthrough/01-index.ts src/index.ts
cp walkthrough/01-agent.ts src/agent.ts
```

说 hello

```
npx tsx src/index.ts hello
```

```
git add . && git commit -m "add cli and agent loop" && git show HEAD --color=always | cat
```

#### 第 2 章 - 添加计算器工具

现在让我们向我们的 BAML 代理添加一个计算器工具

```
cp walkthrough/02-tool_calculator.baml baml_src/tool_calculator.baml
cp walkthrough/02-agent.baml baml_src/agent.baml
```

```
npx baml-cli generate
```

TS 文件无需更改

```
npx tsx src/index.ts 'can you add 3 and 4?'
```

```
git add . && git commit -m "add calculator tools" && git show HEAD --color=always | cat
```

### 第 3 章 - 在循环中处理工具调用

现在让我们添加一个真实的代理循环，可以运行工具并从 LLM 获取最终答案。

```
cp walkthrough/03-agent.ts src/agent.ts
```

```
npx tsx src/index.ts 'can you add 3 and 4?'
```

让我们关闭 BAML 日志并再次运行

```
export BAML_LOG=off
# 用 export BAML_LOG=info 重新开启
```

```
npx tsx src/index.ts 'can you add 3 and 4, then add 6 to that result?'
```

注意其他工具还没有工作，因为我们在代理循环中没有处理它们

```
npx tsx src/index.ts 'can you subtract 3 from 4?'
```

为剩余工具添加处理程序

```
cp walkthrough/03b-agent.ts src/agent.ts
```

```
npx tsx src/index.ts 'can you subtract 3 from 4?'
```

```
npx tsx src/index.ts 'can you multiply 3 and 4?'
```

```
npx tsx src/index.ts 'can you multiply 3 and 4, then divide the result by 2 and then add 12 to that result?'
```

```
git add . && git commit -m "add agent loop" && git show HEAD --color=always | cat
```

### 第 4 章 - 向 agent.baml 添加测试

```
cp walkthrough/04-agent.baml baml_src/agent.baml
```

在 playground 中尝试

```
npx baml-cli test
```

添加一个失败的 assert 并再次测试

```
npx baml-cli test
```

更改 assert 以通过

```
cp walkthrough/04b-agent.baml baml_src/agent.baml
```

现在让我们构建一个带有更复杂工具调用的测试

```
BAML_LOG=info npx tsx src/index.ts 'can you multiply 3 and 4, then divide the result by 2 and then add 12 to that result?'
```

将输出中的线程复制到另一个测试

```
cp walkthrough/04c-agent.baml baml_src/agent.baml
```

```
npx baml-cli test
```

```
git add . && git commit -m "add tests to agent.baml" && git show HEAD --color=always | cat
```

### 第 5 章 - 多个人类工具

```
cp walkthrough/05-agent.baml baml_src/agent.baml
```

```
npx baml-cli generate
```

我们可以通过向 LLM 发送 garbled 消息来测试 `request_more_information` 意图。

```
npx tsx src/index.ts 'can you multiply 3 and FD*(#F&x& ?'
```

更新我们的 CLI 循环，如果代理返回 `request_more_information` 意图，则询问人类输入

```
cp walkthrough/05-agent.ts src/agent.ts
cp walkthrough/05-cli.ts src/cli.ts
```

```
npx tsx src/index.ts 'can you multiply 3 and FD*(#F&& ?'
```

为这种行为添加一些测试

```
cp walkthrough/05b-agent.baml baml_src/agent.baml
```

```
npx baml-cli test
```

看起来我们也破坏了我们的 hello world 测试，让我们修复它

```
cp walkthrough/05c-agent.baml baml_src/agent.baml
```

```
npx baml-cli test
```

```
git add . && git commit -m "add request more information and fix tests" && git show HEAD --color=always | cat
```

### 第 6 章 - 使用推理自定义您的提示

如果我们想使我们的提示更好，让我们添加一些推理

```
cp walkthrough/06-agent.baml baml_src/agent.baml
```

```
npx baml-cli generate
```

>        始终首先思考下一步该做什么，比如
>
>        - ...
>        - ...
>        - ...

```
git add . && git commit -m "add reasoning to agent.baml" && git show HEAD --color=always | cat
```

### 第 7 章 - 自定义您的上下文窗口

我们的上下文窗口可以更好，让我们
演示上下文窗口自定义

- json 显示 indent=2

```
cp walkthrough/07-agent.ts src/agent.ts
```

```
BAML_LOG=info npx tsx src/index.ts 'can you multiply 3 and 4, then divide the result by 2 and then add 12 to that result?'
```

混合 xml

```
cp walkthrough/07b-agent.ts src/agent.ts
```

```
BAML_LOG=info npx tsx src/index.ts 'can you multiply 3 and 4, then divide the result by 2 and then add 12 to that result?'
```

更新测试

```
cp walkthrough/07c-agent.baml baml_src/agent.baml
```

```
npx baml-cli test
```

### 第 8 章 - 添加 API 端点

首先，让我们添加所需的依赖：

```bash
npm install express
npm install --save-dev @types/express supertest
```

现在让我们创建我们的 API 服务器：

```bash
cp walkthrough/08-server.ts src/server.ts
```

您现在可以启动服务器：

```bash
npx tsx src/server.ts
```

在另一个终端中，您可以尝试：

```bash
curl -X POST http://localhost:3000/thread \
  -H "Content-Type: application/json" \
  -d '{"message":"can you add 3 and 4?"}'
```

运行测试：

```
git add . && git commit -m "add api endpoints" && git show HEAD --color=always | cat
```

### 第 9 章 - 内存状态和异步澄清

现在让我们添加状态管理和异步澄清支持：

```bash
cp walkthrough/09-state.ts src/state.ts
cp walkthrough/09-server.ts src/server.ts
```

尝试澄清流程：

```bash
# 使用不清晰输入启动线程
curl -X POST http://localhost:3000/thread \
  -H "Content-Type: application/json" \
  -d '{"message":"can you multiply 3 and xyz?"}'

# 您将得到带有 response_url 的响应 - 使用该 URL 发送澄清
curl -X POST 'http://localhost:3000/thread/{thread_id}/response' \
  -H "Content-Type: application/json" \
  -d '{"message":"lets use 5 instead of xyz"}'
```

### 第 10 章 - 添加人类批准

```
cp walkthrough/10-server.ts src/server.ts
cp walkthrough/10-agent.ts src/agent.ts
```

### 清理

```
rm src/*.ts
rm -r baml_src
```

```
git add . && git commit -m "clean up" && git show HEAD --color=always | cat
```
