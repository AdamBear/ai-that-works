---
"guid": "aitw-002"
"title": "S01E02 – Reasoning Models vs Reasoning Prompts"
"description": "Models can reason but you can also reason within a prompt. Which technique wins out when and why? We'll find out by adding reasoning to an existing movie chat agent."
"event_link": "https://lu.ma/odkhq9a9"
"eventDate": "2025-04-08T18:00:00Z"
"media":
  "url": "https://youtu.be/D-pcKduKdYM"
  "type": "video/youtube"
"links":
  "youtube": "https://youtu.be/D-pcKduKdYM"
  "code": "https://github.com/BoundaryML/ai-that-works/tree/main/2025-04-07-reasoning-models-vs-prompts"
"season": 1
"episode": 2
"event_type": "episode"
---

# 🦄 reasoning models vs reasoning prompts

> models can reason but you can also reason within a prompt. which technique wins out when and why? we'll find out by adding reasoning to an existing movie chat agent.

[Video](https://youtu.be/D-pcKduKdYM)

[![image](https://img.youtube.com/vi/D-pcKduKdYM/0.jpg)](https://youtu.be/D-pcKduKdYM)

## Running this code

```bash
# Install dependencies
pnpm install
```

```bash
# Convert BAML files -> TypeScript
pnpm run generate
```

```bash
# Run the code
pnpm run dev
```

## Followup Exercises

What workflows do you have that you can add reasoning to?

What reasoning workflows can you replace with smaller cheaper models?

## Session Notes

### Key Takeaways

- You can make a cheap model do reasoning just by prompting it well
- Time management of your Engineering Team
     - o3 / reasoning model if you just wanna move fast
- Cost management / speed corollary
     - if you need performance / speed / choice 
     - if you can only run small models e.g. OSS or at the edge
- better prompts / guided reasoning, better than generic <THINK> 
  tokens in general-purpose models
     - you can make a good reasoning model even better with guided reasoning
- actor / checker / llm-as-judge workflows may work but are exponential in cost / latency


![image](https://github.com/user-attachments/assets/7fefd512-b488-437a-8ed1-f64024f6c781)



![image](https://github.com/user-attachments/assets/d01d797f-ee23-4e15-a3b5-58547ac33768)




![image](https://github.com/user-attachments/assets/f73d3db8-79d2-4f29-bb4f-758870e86c72)



![image](https://github.com/user-attachments/assets/b7290e01-ee31-4378-8943-fbd27ab2b0f3)



![image](https://github.com/user-attachments/assets/201380ad-837b-4dc7-8b49-9f7ba350ebbf)


![image](https://github.com/user-attachments/assets/365a92ae-a6e5-41b5-ad00-720b9abf4697)

