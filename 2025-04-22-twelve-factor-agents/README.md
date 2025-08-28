---
"guid": "aitw-004"
"title": "S01E04 – Twelve Factor Agents"
"description": "Learn how to build production-ready AI agents using the twelve-factor methodology. We'll cover the core concepts and build a real agent from scratch."
"event_link": "https://lu.ma/f1cvksud"
"eventDate": "2025-04-22T18:00:00Z"
"media":
  "url": "https://youtu.be/yxJDyQ8v6P0"
  "type": "video/youtube"
"links":
  "youtube": "https://youtu.be/yxJDyQ8v6P0"
  "code": "https://github.com/BoundaryML/ai-that-works/tree/main/2025-04-22-twelve-factor-agents"
"season": 1
"episode": 4
"event_type": "episode"
---

# Building a 12 Factor Agent 

> In this episode, we dove deep on the theory behind 12 factor agents, before getting hands on and building one from scratch

[Video](https://youtu.be/yxJDyQ8v6P0) 

For a full deep dive of the concepts and visuals, check out [12-factor-agents](https://hlyr.dev/12fa)

[![12 Factor Agents Video](https://img.youtube.com/vi/yxJDyQ8v6P0/0.jpg)](https://www.youtube.com/watch?v=yxJDyQ8v6P0)


## How to use this code

There are a few ways to use the code in this folder, the final result is in `final/` and the step by step walkthrough is in `step-by-step/`.

```
.
├── README.md
├── final
│   ├── baml_src
│   │   ├── agent.baml
│   │   └── ...
│   ├── src
│   │   ├── agent.ts
│   │   └── ...
│   ├── package-lock.json
│   ├── package.json
│   └── tsconfig.json
└── step-by-step
    ├── walkthrough
    │   ├── 00-index.ts
    │   ├── 01-agent.baml
    │   ├── 01-agent.ts
    │   ├── ...more files...
    │   └── 10-server.ts
    ├── package-lock.json
    ├── package.json
    ├── tsconfig.json
    └── walkthrough.md
```


### final results

if you just want to run the final result of all our coding, use the code in `final/` 

```bash
cd final
npm install
```

use the cli with

```bash
npx tsx src/index.ts 'hello world'
```

or run the server with

```bash
npx tsx src/server.ts
```

### step by step walkthrough

if you want to walk through the code step by step, use the code in `step-by-step/`

```bash
cd step-by-step
npm install
```

then follow the steps in [step-by-step/walkthrough.md](step-by-step/walkthrough.md) one by one
