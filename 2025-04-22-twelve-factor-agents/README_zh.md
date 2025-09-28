# 构建 12 因素代理

> 在这一集中，我们深入探讨了 12 因素代理背后的理论，然后动手从头构建一个。

[视频](https://youtu.be/yxJDyQ8v6P0)

有关概念和视觉效果的完整深入探讨，请查看 [12-factor-agents](https://hlyr.dev/12fa)

[![12 因素代理视频](https://img.youtube.com/vi/yxJDyQ8v6P0/0.jpg)](https://www.youtube.com/watch?v=yxJDyQ8v6P0)

## 如何使用此代码

此文件夹中的代码有几种使用方式，最终结果在 `final/` 中，逐步演练在 `step-by-step/` 中。

```
.
├── README.md
├── final
│   ├── baml_src
│   │   ├── agent.baml
│   │   └── ...
│   ├── src
│   │   ├── agent.ts
│   │   └── ...
│   ├── package-lock.json
│   ├── package.json
│   └── tsconfig.json
└── step-by-step
    ├── walkthrough
    │   ├── 00-index.ts
    │   ├── 01-agent.baml
    │   ├── 01-agent.ts
    │   ├── ...更多文件...
    │   └── 10-server.ts
    ├── package-lock.json
    ├── package.json
    ├── tsconfig.json
    └── walkthrough.md
```

### 最终结果

如果您只想运行我们所有编码的最终结果，请使用 `final/` 中的代码

```bash
cd final
npm install
```

使用 CLI：

```bash
npx tsx src/index.ts 'hello world'
```

或运行服务器：

```bash
npx tsx src/server.ts
```

### 逐步演练

如果您想逐步演练代码，请使用 `step-by-step/` 中的代码

```bash
cd step-by-step
npm install
```

然后按照 [step-by-step/walkthrough.md](step-by-step/walkthrough.md) 中的步骤一个一个跟随
