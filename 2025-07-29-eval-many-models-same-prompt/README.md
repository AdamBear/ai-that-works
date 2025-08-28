---
"guid": "aitw-016"
"title": "S02E12 – Evaluating Prompts Across Models"
"description": "AI That Works #16 will be a super-practical deep dive into real-world examples and techniques for evaluating a single prompt against multiple models. While this is a commonly heralded use case for Evals, e.g. 'how do we know if the new model is better' / 'how do we know if the new model breaks anything', there's not a ton of practical examples out there for real-world use cases."
"event_link": "https://lu.ma/gnvx0iic"
"eventDate": "2025-07-29T18:00:00Z"
"media":
  "url": "https://www.youtube.com/watch?v=OawyQOrlubM"
  "type": "video/youtube"
"links":
  "youtube": "https://www.youtube.com/watch?v=OawyQOrlubM"
  "code": "https://github.com/BoundaryML/ai-that-works/tree/main/2025-07-29-eval-many-models-same-prompt"
"season": 2
"episode": 12
"event_type": "episode"
---

# 🦄 ai that works: Evaluating Prompts Across Models

> A practical deep dive into evaluating single prompts against multiple models for real-world use cases

[Video](https://www.youtube.com/watch?v=OawyQOrlubM) (1h)

[![Evaluating Prompts Across Models](https://img.youtube.com/vi/OawyQOrlubM/0.jpg)](https://www.youtube.com/watch?v=OawyQOrlubM)

## Episode Summary

This week's session focused on systematically deciding which LLM is right for your specific use case. We demonstrated how to build a simple evaluation tool to benchmark models side-by-side on your specific prompts, weighing output quality against latency and cost.

### Key Points
1. Be open to trying new models but ensure they fit your specific needs before adopting them.
2. Automate evaluations when possible to minimize the manual effort involved in testing.
3. Consider the business use case when defining what constitutes 'accuracy' in AI generated outputs.
4. Build tools to simplify the evaluation of multiple models and prompt variations to streamline the analysis process.

### Main Topics
- Model evaluation strategies
- User experience in AI applications
- Benchmarking LLM performance
- Prompt engineering and its impact on model accuracy

## Key Takeaways

- **Evaluate new LLM models based on performance, cost, and speed.** When a new model drops, don't just look at its upper bound - benchmark it against your specific use cases.

- **User experience often drives the decision to switch models.** A slightly "less accurate" but significantly faster model can often provide a better user experience. Automating these evaluations allows you to confidently decide when a model switch is justified by both the metrics and the end-user's delight.

- **Build bespoke evaluation tools.** Vibe code UIs that help you understand the comparisons you need to make. Model vs Model for the same prompt/task. Task vs Task for the same model/prompt. Prompt vs Prompt for the same task/model. There's a lot of parameterization, don't get overwhelmed and make a 1 tool for everything. Bespoke tools all the way (at least when you start).

- **Establish personal benchmarks to assess new models effectively.** The importance of context engineering and iterative evaluation in improving model outputs.

## The One Thing to Remember

> Systematically evaluate new models against your own benchmarks for performance, cost, and speed. The 'best' model is the one that best serves your specific use case and user experience.

## Running the Code

- `bun run index.ts`
- OR `npx tsx index.ts`
- `uv run main.py`

## Resources

- [Session Recording](https://www.youtube.com/watch?v=OawyQOrlubM)
- [Discord Community](https://boundaryml.com/discord)
- Sign up for the next session on [Luma](https://lu.ma/baml)

## Whiteboards

## Links