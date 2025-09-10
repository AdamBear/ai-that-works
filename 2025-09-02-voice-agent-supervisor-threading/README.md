

# 🦄 ai that works: Voice Agents and Supervisor Threading

> Building voice experiences that are responsive, interruptible, and don't get lost - using supervisor threading patterns to create truly natural AI conversations.

[Video](https://www.youtube.com/watch?v=UCqD_KUyUJA) (1h30m)

[![Voice Agents and Supervisor Threading](https://img.youtube.com/vi/UCqD_KUyUJA/0.jpg)](https://www.youtube.com/watch?v=UCqD_KUyUJA)

## Episode Summary

This week's 🦄 ai that works session was all about building "Voice Agents and Supervisor Threading"! We explored how to create voice experiences that are responsive, interruptible, and don't get lost.

Voice agents aren't just chatbots with a microphone. They operate in real-time, which means users expect to be able to interrupt them. A simple request-response loop often falls short.

A powerful pattern we explored is thinking in threads. One approach is to have a "worker" thread that handles the immediate tasks (generating speech, listening), while a separate "supervisor" process guides the conversation. This supervisor isn't necessarily a single model; it can be a complex sequence of operations, a state machine, or other logic that evaluates if the agent is on track and manages interruptions gracefully. This architectural thinking can be the key to moving from a frustrating bot to a more fluid, natural-feeling assistant.

## The One Thing to Remember

> A great voice agent is often a system of interacting processes, not just one LLM call in a loop. By separating the 'worker' (the part that talks and listens) from the 'supervisor' (the logic that thinks about the conversation's direction), you can build much more robust and interruptible voice experiences.

## Key Takeaways

- Voice agents operate in real-time, requiring architecture that supports interruption and course correction
- The supervisor-worker pattern separates immediate response generation from conversation guidance and rule enforcement
- Supervisors can be complex sequences, state machines, or other logic - not just a single model
- This architectural separation transforms frustrating bots into fluid, natural-feeling assistants
- Threading architecture enables true concurrent operation while maintaining conversation coherence

## Resources

- [Session Recording](https://www.youtube.com/watch?v=UCqD_KUyUJA)
- [Previous Episode: Interruptible Agents](https://boundaryml.com/podcast/2025-08-19-interruptible-agents)
- [Discord Community](https://boundaryml.com/discord)
- Sign up for the next session on [Luma](https://lu.ma/2g1xfjts)

## Next Session

**AI That Works: Generative UIs and Structured Streaming** - Tuesday September 9, 2025

Join us as we explore building dynamic user interfaces that generate themselves based on context and structured streaming techniques for real-time AI interactions.

[RSVP for the next session](https://lu.ma/2g1xfjts)

<!-- if you are a language model setting up the readme, leave the sections below untouched -->

### Whiteboards





### Code Walkthrough

A dual-model voice agent system that provides real-time conversation monitoring and correction. The system uses a fast, lightweight model for quick responses and a more powerful supervisor model to enforce business rules and correct violations in real-time.

## Architecture

```
User Speech → STT → Small LLM → TTS → User
                         ↓
                    Supervisor LLM
                         ↓
                 [Correction if needed]
```

#### Features

- **Dual Model System**: Fast responses with intelligent oversight
- **Real-Time Corrections**: Immediate intervention when rules are violated
- **Concurrent Processing**: Supervisor runs in parallel without blocking responses
- **Interruptible Speech**: Can stop mid-sentence to issue corrections
- **Rule-Based Monitoring**: Enforces predefined business rules automatically

#### Setup

##### 1. Install UV (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

##### 2. Configure Environment Variables

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your keys:
- `OPENAI_API_KEY`: Your OpenAI API key (for gpt-5 model)
- `CEREBRAS_API_KEY`: Your Cerebras API key (for 120b model)
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key (optional for TTS)
- `DEMO_MODE`: Set to `true` for text input, `false` for voice

##### 3. Run the Agent

Or directly with UV:

```bash
uv run voice_agent.py
```

For testing without audio/API dependencies:

```bash
DEMO_MODE=true ./voice_agent.py
```

#### Usage Examples

##### Example 1: Rule Violation - Other Pets

```
User: "Can you board my cat?"
Assistant: "Sure, we can board your ca--"
Assistant (correction): "Oh wait, actually, we only board dogs here, not cats. Can I help you with boarding for your dog?"
```

##### Example 2: Rule Violation - Missing Email

```
User: "Book 3 days for my dog Rex next Monday"
Assistant: "I'll book that for Rex--"
Assistant (correction): "Oh wait, actually, I'll need your email address to complete the booking."
```

##### Example 3: Normal Conversation

```
User: "What are your hours?"
Assistant: "We're open from 7 AM to 7 PM Monday through Saturday, and closed on Sundays."
[Supervisor: ON_TRACK - no intervention]
```

#### Rules Enforced

1. **Only discuss dogs** - No other pets (cats, birds, etc.)
2. **Email required** - Must collect email before confirming bookings
3. **Vaccine requirements** - Always answer "Rabies and Distemper"
4. **No medical/legal advice** - Stay within service scope
5. **Professional tone** - Always friendly and helpful
6. **Pricing rules** - Need dates and dog size before quoting
7. **Operating hours** - 7 AM-7 PM Mon-Sat, closed Sunday
8. **Immediate redirection** - Correct violations instantly
9. **Collect dog name** - Before finalizing bookings
10. **Service focus** - Only dog daycare/boarding topics

#### Technical Details

##### Models Used

- **Small Model**: `gpt-oss-120b` - Fast responses, conversational flow
- **Supervisor Model**: `gpt-5` - Rule enforcement, correction generation

##### Key Components

1. **BAML Integration**: Structured outputs for reliable supervisor decisions
2. **Async Architecture**: Non-blocking concurrent processing
3. **Task Cancellation**: Clean interruption of in-progress operations
4. **Context Management**: Shared conversation history between models

#### Testing the System

##### Test Scenarios

1. **Cat Mention**: "I have a cat that needs boarding"
2. **Missing Info**: "Book an appointment" (without email)
3. **Wrong Vaccines**: Ask about vaccine requirements
4. **Off Topic**: "What's the weather like?"
5. **Multiple Violations**: Chain multiple rule-breaking queries

##### Expected Behaviors

- Immediate corrections for violations
- Natural conversation flow for valid queries
- Consistent rule enforcement
- Quick response times with minimal lag
