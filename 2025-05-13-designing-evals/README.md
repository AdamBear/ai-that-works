---
"guid": "aitw-005"
"title": "S02E01 – Designing Evals"
"description": "Minimalist and high-performance testing/evals for LLM applications. Stay tuned for our season 2 kickoff topic on testing and evaluation strategies."
"event_link": "https://lu.ma/j5y6bd3i"
"eventDate": "2025-05-13T18:00:00Z"
"media":
  "url": "https://youtu.be/-N6MajRfqYw"
  "type": "video/youtube"
"links":
  "youtube": "https://youtu.be/-N6MajRfqYw"
  "rsvp": "https://lu.ma/j5y6bd3i"
  "code": "https://github.com/BoundaryML/ai-that-works/tree/main/2025-05-13-designing-evals"
"season": 2
"episode": 1
"event_type": "episode"
---

# 🦄 designing evals

> minimalist and high-performance testing/evals for LLM applications

[Video](https://youtu.be/-N6MajRfqYw) • [RSVP](https://lu.ma/j5y6bd3i)

## Overview

This session explores best practices for evaluating LLM applications, focusing on practical, efficient approaches that provide meaningful insights without unnecessary complexity.

## Running this code

### installing dependencies

```bash
# Install dependencies
uv sync
```

### run the code

```
# Run the code
python hello.py
```

## Key Topics

1. Why evals are great - what you can do with an answer key
2. How to get the answer key
    1. we all start out with no answer key
    2. how do you build it up over time
3. Structured Data vs. Unstructured data
    1. people view as one or the other, but its often semi-structured / a blend
    2. json with sentences
    3. markdown with json
4. using rubrics to design evals
5. llm as judge
6. Enron email dataset
7. Visualizing Eval Results

## Session Notes

Checklist

- Vibe evals - run your prompt (e.g. in playground) and look at the output
    - write in a few test cases that work
    - write a few end to end tests that run your prompt chain (e.g. with pytest)
    - great for tone
- capture intermediate steps of your pipeline as probes and individual testable components
    - alternative to probes 
- structured outputs from an llm
    - helps you break your problems down into smaller components
    - e.g. lesson plan output --> "list of biases", "estimated cost"
- don't use numbers for confidence, use a rubric
    - categorical, "slow" vs "medium" vs "fast" - enum-based evals
- use prod data to build up your golden dataset over time
    - review diffs in either/both of RAW OUTPUT and the STRUCTURED EVALUATION of your pipeline outputs


## Links

- (using only) integrated tests are a scam [https://www.youtube.com/watch?v=VDfX44fZoMc](https://www.youtube.com/watch?v=VDfX44fZoMc)
- [V0 - visualization for EVALS](https://v0.dev/chat/4uFXuYz2TEn)

## whiteboards

![image](https://github.com/user-attachments/assets/76c48baf-a4d5-4607-9a67-88ea27687d27)

![image](https://github.com/user-attachments/assets/a3eb3a6f-da46-47b8-a721-de0d551e57c7)

![image](https://github.com/user-attachments/assets/fb54a84e-a185-4325-aa02-00167db70317)

![image](https://github.com/user-attachments/assets/135d9f07-f195-4d79-95d6-6abf501d11ac)

