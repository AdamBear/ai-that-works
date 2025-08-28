---
"guid": "aitw-003"
"title": "S01E03 – Code Generation with Small Models"
"description": "Large models can do a lot, but so can small models. We'll discuss techniques for how to leverage extremely small models for generating diffs and making changes in complete codebases."
"event_link": "https://lu.ma/jvq3ug1g"
"eventDate": "2025-04-15T18:00:00Z"
"media":
  "url": "https://youtu.be/KJkvYdGEnAY"
  "type": "video/youtube"
"links":
  "youtube": "https://youtu.be/KJkvYdGEnAY"
  "code": "https://github.com/BoundaryML/ai-that-works/tree/main/2025-04-15-code-generation-small-models"
"season": 1
"episode": 3
"event_type": "episode"
---

# 🦄 code generation with small models

> large models can do a lot, but so can small models. we'll discuss techniques for how to leverage extremely small models for generating diffs and making changes in complete codebases.

## Diagrams

### Overall Ownership - User vs. Agent

![image](https://github.com/user-attachments/assets/658a465d-de6b-4f0e-8aa6-5a1f5aa85613)

### Architecture

![image](https://github.com/user-attachments/assets/ec88c07b-21fc-430d-a065-4654dfd280fa)

### Context Window Management

![image](https://github.com/user-attachments/assets/d0e37f92-9b6d-4de7-bf50-e2e960203927)


### Pipelining Updates

![image](https://github.com/user-attachments/assets/9898929e-cbf9-4418-aeb9-8d767b703acb)

### Optimize - Serve most users with small, fast models 

![image](https://github.com/user-attachments/assets/a4cd3df8-56f8-49b6-b1d8-12331f1d4825)

### Start with big expensive models, improve coverage with smaller models over time

![image](https://github.com/user-attachments/assets/8712b167-c937-4bfb-8629-60ac36f9f70b)



## Project Structure

This session contains two main components:

### 1. Calculator Project (`/project`)
A simple calculator application that demonstrates a complete, well-structured Python codebase. Features include:
- Basic arithmetic operations (+, -, *, /)
- Memory functionality (store, recall, clear)
- Interactive command-line interface
- Clean separation of concerns (operations, calculator logic, user interface)

### 2. Agent Project (`/agent`)
A BAML-based project that shows how to use small models to generate and modify code. The agent demonstrates:
- Code analysis and understanding
- Targeted code modifications
- Working with existing codebases

## Running the Code

### Calculator Project
```bash
cd project

# Install dependencies
uv sync

# Run the calculator
python main.py
```

### Agent Project
```bash
cd agent

# Install dependencies
uv sync

# Generate BAML code
uv run baml-cli generate

# Run the agent
python hello.py
```
