# 🦄 使用小模型进行代码生成

> 大型模型可以做很多，但小型模型也可以。我们将讨论如何利用极小模型生成差异并在完整代码库中进行更改的技术。

## 图表

### 总体所有权 - 用户 vs. 代理

![image](https://github.com/user-attachments/assets/658a465d-de6b-4f0e-8aa6-5a1f5aa85613)

### 架构

![image](https://github.com/user-attachments/assets/ec88c07b-21fc-430d-a065-4654dfd280fa)

### 上下文窗口管理

![image](https://github.com/user-attachments/assets/d0e37f92-9b6d-4de7-bf50-e2e960203927)

### 管道化更新

![image](https://github.com/user-attachments/assets/9898929e-cbf9-4418-aeb9-8d767b703acb)

### 优化 - 使用小而快的模型服务大多数用户

![image](https://github.com/user-attachments/assets/a4cd3df8-56f8-49b6-b1d8-12331f1d4825)

### 从大型昂贵的模型开始，随着时间推移用更小的模型改进覆盖率

![image](https://github.com/user-attachments/assets/8712b167-c937-4bfb-8629-60ac36f9f70b)

## 项目结构

此会话包含两个主要组件：

### 1. 计算器项目 (`/project`)

一个简单的计算器应用程序，演示完整的、结构良好的 Python 代码库。功能包括：

- 基本算术运算 (+, -, *, /)

- 内存功能 (存储、回忆、清空)

- 交互式命令行界面

- 关注点分离 (操作、计算器逻辑、用户界面)

### 2. 代理项目 (`/agent`)

基于 BAML 的项目，展示如何使用小模型生成和修改代码。代理演示：

- 代码分析和理解

- 针对性代码修改

- 与现有代码库合作

## 运行代码

### 计算器项目

```bash
cd project

# 安装依赖
uv sync

# 运行计算器
python main.py
```

### 代理项目

```bash
cd agent

# 安装依赖
uv sync

# 生成 BAML 代码
uv run baml-cli generate

# 运行代理
python hello.py
```
