---
"guid": "aitw-014"
"title": "S02E10 – Implementing Decaying-Resolution Memory"
"description": "Last week on #13, we did a conceptual deep dive on context engineering and memory - this week, we're going to jump right into the weeds and implement a version of Decaying-Resolution Memory that you can pick up and apply to your AI Agents today. For this episode, you'll probably want to check out episode #13 in the session listing to get caught up on DRM and why its worth building from scratch."
"event_link": "https://lu.ma/qz7gson7"
"eventDate": "2025-07-15T18:00:00Z"
"media":
  "url": "https://www.youtube.com/watch?v=CEGSDlCtI8U"
  "type": "video/youtube"
"links":
  "youtube": "https://www.youtube.com/watch?v=CEGSDlCtI8U"
  "code": "https://github.com/BoundaryML/ai-that-works/tree/main/2025-07-15-decaying-resolution-memory"
"season": 2
"episode": 10
"event_type": "episode"
---

# 🦄 ai that works: Implementing Decaying-Resolution Memory

> A hands-on implementation of Decaying-Resolution Memory (DRM) for AI agents, building on the conceptual foundation from episode #13 to create a practical, deployable memory system.

[Watch on YouTube](https://www.youtube.com/watch?v=CEGSDlCtI8U)

## Episode Highlights

Moving from theory to practice - implementing DRM as a production-ready component you can integrate into your agents today.

The key insight of DRM is that not all memories need the same resolution over time. Recent events stay detailed, while older events naturally compress into higher-level summaries.

By implementing exponential decay in memory resolution, we create a system that mirrors human memory - preserving what matters while gracefully forgetting the details that don't.

## Whiteboards

<img width="3706" height="1857" alt="image" src="https://github.com/user-attachments/assets/2dbabf09-56eb-4238-9ec2-88ab5fa509ad" />

<img width="5133" height="2113" alt="image" src="https://github.com/user-attachments/assets/2414ad6f-0a0b-4b1e-a658-4695d955454f" />

<img width="3705" height="2970" alt="image" src="https://github.com/user-attachments/assets/3000b593-6649-4a20-a431-25c46abeb963" />

<img width="3826" height="3153" alt="image" src="https://github.com/user-attachments/assets/2c489058-01bb-4b85-9345-6282e63235e4" />

<img width="2738" height="2722" alt="image" src="https://github.com/user-attachments/assets/6defe4e1-44ce-4313-bc8c-ade5000246e3" />


## Key Takeaways

- Decaying-Resolution Memory provides a scalable approach to agent memory by automatically summarizing and compressing information over time
- The implementation focuses on practical concerns: storage efficiency, retrieval speed, and maintaining semantic coherence across different time resolutions
- Building on episode #13's conceptual framework, this session delivers working code that can be adapted to various agent architectures

## Resources

- [Session Recording](https://www.youtube.com/watch?v=CEGSDlCtI8U)
- [Previous Episode: Building AI with Memory & Context](../2025-07-08-context-engineering)
- [Discord Community](https://boundaryml.com/discord)
- Sign up for the next session on [Luma](https://lu.ma/baml)

## Next Session

**AI That Works #15: PDF Processing** - July 22, 2025

Join us next week as we dive deep into practical PDF processing techniques for AI applications. We'll explore how to extract, parse, and leverage PDF content effectively in your AI workflows, tackling common challenges like layout preservation, table extraction, and multi-modal content handling.

[RSVP for the PDF Processing session](https://lu.ma/75ijhvs8)
