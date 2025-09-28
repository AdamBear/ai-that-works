# 🦄 推理模型 vs 推理提示

> 模型可以推理，但您也可以在提示中进行推理。哪种技术在何时获胜以及为什么？我们将通过向现有的电影聊天代理添加推理来找出答案。

[视频](https://youtu.be/D-pcKduKdYM)

[![image](https://img.youtube.com/vi/D-pcKduKdYM/0.jpg)](https://youtu.be/D-pcKduKdYM)

## 运行此代码

```bash
# 安装依赖
pnpm install
```

```bash
# 将 BAML 文件转换为 TypeScript
pnpm run generate
```

```bash
# 运行代码
pnpm run dev
```

## 后续练习

您有哪些工作流程可以添加推理？

您可以用哪些推理工作流程替换更小、更便宜的模型？

## 会话笔记

### 关键要点

- 您可以通过良好提示使廉价模型进行推理
- 工程团队的时间管理
  - o3 / 推理模型如果您只想快速前进
- 成本管理 / 速度推论
  - 如果您需要性能 / 速度 / 选择
  - 如果您只能运行小模型，例如 OSS 或边缘
- 更好的提示 / 引导推理，比通用 <THINK> 令牌更好
  - 您可以用引导推理使好的推理模型更好
- 演员 / 检查器 / llm-as-judge 工作流程可能有效，但成本 / 延迟呈指数增长

![image](https://github.com/user-attachments/assets/7fefd512-b488-437a-8ed1-f64024f6c781)

![image](https://github.com/user-attachments/assets/d01d797f-ee23-4e15-a3b5-58547ac33768)

![image](https://github.com/user-attachments/assets/f73d3db8-79d2-4f29-bb4f-758870e86c72)

![image](https://github.com/user-attachments/assets/b7290e01-ee31-4378-8943-fbd27ab2b0f3)

![image](https://github.com/user-attachments/assets/201380ad-837b-4dc7-8b49-9f7ba350ebbf)

![image](https://github.com/user-attachments/assets/365a92ae-a6e5-41b5-ad00-720b9abf4697)
