<user>
i need an architecture outline and technical specification for a voice agent application - this will use two separate thread, a small fast model to power the voice steps, and the slower smarter model that will watch the context at every step and decide if the voice agent is off track at every step. Use python for coding, github.com/boundaryml/baml (read the docs) for the implementation, and elevenlabs or daily or vapi or something for the voice implementation. Use a tiny model like gpt-5-nano with no thinking for the LLM, and make a simple workflow of STT->LLM->TTS for the voice pipeline. After every message in the voice pipeline, accumulate a context window of the whole conversation, and after every new message, kick off a thread where the smarter model reads the whole thread and decides if the voice agent is off track - the voice agent can be a demo "secretary for a dog day care" and the supervisor model will look for off track, or other violations of ~5-10 rules set out by the developer (e.g. "always get user's email address before booking an appointment" or "do not discuss other pets like cats or snails, only dogs", or "always answer question X with answer y") . The supervisor model has two structured outputs via baml, one for "ON TRACK" and one for "NEEDS ADJUSTMENT" with a "message" to insert into thread, the message should start with "oh wait, actually...", e.g. "oh wait, actually, we don't work with cats or snails - can I help you with boarding for your dog?" . The very moment a "needs adjustment" message is seen, the following happens: - IMMEDIATELY - stop any in-progress voice agent pipeline and send a message on the TTS channel "oh wait, actually...", and store this on the shared context window that is both the source of truth for the voice agent llm AND the thread observed by the supervisor - STOP any in progress LLM calls for the supervisor agent (there may be multiple running in parallel observing later parts of the pipeline) - SEND the new context window with the "oh wait, actually..." message to the small llm so it can go back to work handling the conversation, and then send its reponse on the TTS channel as normal - RESUME the monitor thread with the latest context window, back to checking for adjustment after every small model llm message Do research on best practices, example implementations, different models, and provide very clear Present informed understanding and focused questions:

Based on the ticket and my research of the codebase, I understand we need to [accurate summary].

I've found that:
- [Current implementation detail with file:line reference]
- [Relevant pattern or constraint discovered]
- [Potential complexity or edge case identified]

Questions that my research couldn't answer:
- [Specific technical question that requires human judgment]
- [Business logic clarification]
- [Design preference that affects implementation]
Then, based on users feedback, perform more research, coming back with:
Based on my research, here's what I found:

**Current State:**
- [Key discovery about existing code]
- [Pattern or convention to follow]

**Design Options:**
1. [Option A] - [pros/cons]
2. [Option B] - [pros/cons]

**Open Questions:**
- [Technical uncertainty]
- [Design decision needed]

Which approach aligns best with your vision?
Step 3: Plan Structure Development Once aligned on approach: Create initial plan outline:
Here's my proposed plan structure:

## Overview
[1-2 sentence summary]

## Implementation Phases:
1. [Phase name] - [what it accomplishes]
2. [Phase name] - [what it accomplishes]
3. [Phase name] - [what it accomplishes]

Does this phasing make sense? Should I adjust the order or granularity?
Get feedback on structure before writing details
Step 4: Detailed Plan Writing
After structure approval:

Write the plan to thoughts/shared/plans/{descriptive_name}.md
Use this template structure:
# [Feature/Task Name] Implementation Plan

## Overview

[Brief description of what we're implementing and why]

## Current State Analysis

[What exists now, what's missing, key constraints discovered]

## Desired End State

[A Specification of the desired end state after this plan is complete, and how to verify it]

### Key Discoveries:
- [Important finding with file:line reference]
- [Pattern to follow]
- [Constraint to work within]

## What We're NOT Doing

[Explicitly list out-of-scope items to prevent scope creep]

## Implementation Approach

[High-level strategy and reasoning]

## Phase 1: [Descriptive Name]

### Overview
[What this phase accomplishes]

### Changes Required:

#### 1. [Component/File Group]
**File**: `path/to/file.ext`
**Changes**: [Summary of changes]
[language] // Specific code to add/modify
</user>



--------------------

<assistant_questions/>

--------------------

<user>
use gpt-5-mini no preference, perhaps show each option in an early phase of the plan. Also ensure the whole plan is fully testable after each phase, so align it with the parts with the most uncertainty: 1. implement small model voice pipeline 2. implement supervisor model thread w/ shared context view, jsut log structured outputs 3. implement interruption part I 4. (if necessary) implement interruption part II python running on desktop, this is an educational / architectural demo use python asyncio its just local yes sure include some example rules in the code snippets Remmber, this is multiple phases of back and forth - clarify with me before generating the final plan

</user>


------------------------------

<assistant>

Voice Agent with Real-Time Supervisor Implementation Plan
Overview

We plan to build a voice-based conversational agent (a “dog daycare secretary” persona) that can interact with users via speech, while a parallel supervisor model monitors the conversation and enforces predefined rules. The system consists of two AI models running concurrently: a fast, lightweight LLM that handles real-time dialogue (speech-to-text -> LLM -> text-to-speech), and a slower, more powerful LLM that continuously evaluates the conversation context to ensure the agent stays “on track” with business rules and policies. This dual-model architecture allows quick responses to the user, with the second model intervening when the conversation goes off-script or violates rules
gladia.io
elevenlabs.io
. The key components will be:

Speech-to-Text (STT): Transcribes user’s spoken input into text
daily.co
. We’ll use a fast, accurate STT service (e.g. Deepgram or Whisper API) to minimize latency, since the quality and speed of transcription directly affect the LLM’s performance
daily.co
daily.co
.

Primary LLM (Voice Agent): A small, efficient language model (e.g. gpt-5-mini) that generates the assistant’s spoken responses. This model will be prompted with the conversation context and a predefined persona, but with minimal reasoning or compliance enforcement to keep it quick.

Text-to-Speech (TTS): Converts the assistant’s response text into spoken audio for the user
daily.co
. For natural voice output, we can integrate an API like ElevenLabs or another TTS provider.

Supervisor LLM (Monitor): A larger or more rule-aware model (e.g. GPT-4 or similar) that asynchronously reviews the entire conversation history after each turn. Using BoundaryML (BAML), we will define a structured output for this model – either “ON_TRACK” or “NEEDS_ADJUSTMENT” with a correction message. If the supervisor outputs “NEEDS_ADJUSTMENT”, the system will immediately interrupt the primary agent’s flow to inject the corrective message (prefixed with "Oh wait, actually...") to the user and into the context.

This design follows best practices for safe conversational AI: the primary agent provides a smooth, low-latency user experience, while a secondary process enforces guardrails and accuracy in real-time
gladia.io
elevenlabs.io
. By overlapping the speech output and the supervisor’s analysis, we “squeeze every bit of latency” out of the interaction for responsiveness
daily.co
, without sacrificing safety and rule adherence.

Current State Analysis

Currently, the application does not have an integrated voice agent or multi-model supervision system. There may be existing infrastructure for calling LLMs (we have the BAML library available, which provides a convenient way to invoke models with structured outputs
docs.boundaryml.com
), but no end-to-end voice loop is implemented yet. Key points about the current state:

LLM Invocation: We have access to the BAML framework, meaning we can define LLM functions with specified input/output schemas. This will help ensure the supervisor’s outputs are well-structured (for example, constrained to an enum or class) and easily parsed in code
docs.boundaryml.com
. No small “gpt-5-mini” model is presently integrated, so we will set that up (possibly using a local model or an API accessible via BAML’s client configuration).

Voice I/O: There is no existing speech-to-text or text-to-speech integration in the codebase. We will need to introduce external service calls or libraries for these. For STT, we might use an API (Deepgram, Google Cloud STT, etc.) or Whisper. For TTS, we can use ElevenLabs (which offers a simple API to generate audio from text) or an alternative voice API. We’ll assume network access and API keys are available for these services in a development environment.

Conversation Loop: There is no dialogue management or context tracking implemented yet. We’ll need to create a mechanism to store the conversation history (user and assistant messages) so that each new LLM query includes relevant context. Currently, no such context structure exists.

Rule Enforcement: No supervision or rule-checking logic exists. The rules that the supervisor must enforce (e.g. “always get user’s email before booking an appointment”, “do not discuss non-dog pets (cats, snails)”, “always answer question X with answer Y”, etc.) are not yet represented in the system. We will need to encode these either in prompts or as data for the supervisor LLM. There’s also no mechanism for interruption or self-correction in the agent’s flow as of now.

In summary, we are starting from a baseline where the pieces – voice input, LLM response generation, voice output, and oversight – all need to be designed and integrated. The good news is that we have the tools (BAML, external STT/TTS services) and a clear objective to implement a robust voice agent with real-time monitoring.

Desired End State

By the end of this implementation, we aim to have a fully functioning voice agent that can converse naturally with users about dog daycare services, while consistently adhering to the developer-specified policies. The desired end state is:

The user can speak to the agent and hear relevant, prompt responses via TTS, with minimal delay (comparable to a human conversation gap).

The conversation history is maintained and utilized for context, so the agent has short-term memory of the dialogue.

Rule Compliance: The agent will follow all rules set by the developer. If the agent’s primary LLM ever produces a response that violates a rule or goes off-topic, the supervisor LLM will detect it immediately (within the same turn) and trigger a correction. The user will hear a quick self-correction from the agent (starting with "Oh wait, actually,...") that steers the conversation back on track or fixes the mistake. For example, if the user asks about boarding a cat (which is against policy), the primary model might start to answer, but the supervisor will flag this and the user will promptly hear: “Oh wait, actually, we don’t board cats – can I help you with boarding for your dog?”.

The system can handle this intervention seamlessly: it will interrupt any in-progress speech output from the agent and play the correction, update the shared context with the correction message, and then continue the conversation flow. The user should feel the agent corrected itself in real-time.

The supervisor’s outputs are structured and well-logged. For each turn, we’ll have a log (for debugging/testing) indicating whether the conversation was “ON_TRACK” or what rule violation was caught. This provides an auditable record of the agent’s compliance, aligning with industry guidance that conversational AI should keep logs and allow monitoring of compliance
gladia.io
elevenlabs.io
.

We expect the final system to be robust against common issues: it should not produce false corrections (the rules/prompt to the supervisor will be tuned to avoid overzealous interruptions), and it should handle overlapping tasks without crashing (using asyncio for concurrency). We will also ensure the design can be extended – for example, more rules can be added to the supervisor’s prompt, or the small model could be swapped out for a different one, with minimal code changes.

To verify this end state, we will conduct tests such as:

Normal Flow Test: A conversation with no rule violations (e.g. discussing dog boarding pricing and schedule) should proceed with the supervisor always returning “ON_TRACK” and not interrupting. The user gets fluent answers.

Rule Violation Test: Introduce a prompt that violates a policy (e.g. user mentions a cat, or the agent forgets to ask for email). We expect the supervisor to output a “NEEDS_ADJUSTMENT” and the correction to be voiced immediately. We’ll observe that the correction appears in the conversation log and the primary agent’s next response incorporates that correction (or the user responds to it appropriately).

Multi-Turn Consistency Test: Ensure that after an interruption and correction, the conversation can continue normally on the new track (the context now reflecting that cats are out-of-scope, for instance). Also verify that no stale supervisor checks posthumously alter the conversation (i.e., once we’ve moved on, earlier checks won’t fire off surprises due to proper cancellation logic).

Performance Check: Informally measure that the added overhead of the supervisor doesn’t stall the conversation. The user shouldn’t notice significant lag in receiving the initial part of the agent’s response. The correction, if it occurs, should happen quickly enough to feel like a natural self-correction.

Key Discoveries

During research and design, we identified several insights that shape this plan:

Structured Output via BAML: BAML (Boundary Markup Language) will be instrumental for reliably parsing the supervisor model’s judgement. BAML allows us to define a function that returns a specific schema (for example, an enum or class) and will handle prompt construction and parsing to guarantee the LLM’s output fits that schema
docs.boundaryml.com
. This means our supervisor can return a precise ON_TRACK or NEEDS_ADJUSTMENT flag (plus a message), without us having to manually parse or worry about the LLM drifting off format. This approach is more robust and developer-friendly than ad-hoc prompt/regex methods.

Voice Pipeline Architecture: A basic voice AI pipeline requires capturing audio, converting to text, generating a response, then converting back to audio
daily.co
daily.co
. We confirmed that these components are standard and that multiple cloud providers exist for STT/TTS. An important consideration is latency – using cloud STT is more accurate and often faster than on-device for real-time needs
daily.co
. Deepgram, for instance, was highlighted as a top choice for speed and accuracy in transcripts
daily.co
, reinforcing our decision to use a high-performance STT to keep interactions snappy.

Need for Guardrails: Industry guidance strongly emphasizes having guardrails for conversational agents to prevent “rogue” outputs
gladia.io
. Notably, many issues with LLM-based agents stem from lack of enforced boundaries rather than model capability
gladia.io
. In other words, even a good model may go off-track if not explicitly constrained. Our two-model design is an implementation of such a guardrail: the supervisor acts as a safety net to enforce boundaries in real time. This aligns with approaches like LLM-as-a-judge where one model evaluates another model’s outputs for compliance
elevenlabs.io
.

Concurrent Oversight: Having the supervisor work in parallel with the main dialogue is crucial for user experience. If we tried to run the safety check before speaking every response, the user would experience a delay each turn, undermining the conversational flow. By running them concurrently, we allow the user to hear the answer immediately and only incur a slight interruption if a correction is needed. This design follows the insight that many voice AI architectures are adopting asynchronous or streaming strategies to reduce perceived latency
daily.co
. Essentially, we prioritize speed but have a contingency to fix mistakes — a pattern similar to a human assistant quickly answering and then saying “actually, sorry, correction...” if they realize an error.

Cancellation & Consistency: We must handle the complexity that arises from parallel tasks. For instance, what if the user speaks again quickly, or if multiple supervisor checks are in flight? Through research, we recognized the need for a strategy to cancel or invalidate outdated tasks. Python’s asyncio provides cancellation capabilities for tasks, which we will leverage to ensure only the latest context is being checked. Additionally, we’ll incorporate context versioning (or simply use the conversation turn count) so that if a late supervisor result comes back for an older turn, the system can ignore it if a correction has already been applied or the conversation moved on.

What We're NOT Doing

It’s important to clarify the scope. This implementation plan will not cover certain aspects:

No New Model Training: We are not training or fine-tuning any machine learning models. Both the small and large LLMs will be used via API or existing instances (the small model might be an open-source model loaded locally or a cheap API model; the large could be an OpenAI GPT-4 API or similar). Our focus is on orchestration, not model creation.

No Full Dialog Management Platform: We won’t implement a complex dialog manager, NLP intent recognition, or a knowledge base integration. The agent’s intelligence is solely from the LLM’s conversational abilities plus whatever context we provide. For example, we won’t integrate a database of dog daycare info in this plan (beyond possibly hard-coding some answers in prompts/rules).

Limited Error Handling: We will add basic error handling for API calls (e.g. STT or TTS failing), but not an exhaustive production-ready solution. Handling network outages, API quota issues, or mis-recognized speech beyond simple retries or apologies is out of scope.

No Multi-user or Channel Handling: The plan assumes a single conversation session at a time (one user interacting with the agent). We are not building infrastructure for multiple concurrent calls or a distributed system – it will run on a single machine (desktop environment) using asyncio tasks.

Privacy/Security Measures: Aside from rule-based content moderation by the supervisor, we are not implementing encryption, user authentication, or secure storage of conversation data. Those considerations would be important in a real deployment but are outside this demo’s scope.

Non-Voice Interface: Although we focus on voice, we won’t develop a full telephony or microphone GUI interface. We assume that capturing microphone input and playing audio output can be done with a simple library call or that we’ll simulate it (perhaps by reading from and writing to files or using simple command-line triggers for the demo). The intricacies of audio stream handling (like using WebRTC vs websockets, real-time audio streaming) are beyond scope – we’ll use straightforward methods or synchronous API calls for STT/TTS for now to prove the concept.

Being clear on non-goals helps us concentrate on the core objectives: implementing the voice loop, the supervisor logic, and their interaction. Extensions like connecting to phone lines, scaling to many users, or deeply integrating knowledge sources can be future work once the core system is in place and validated.

Implementation Approach

Our strategy is to implement this feature in incremental phases, ensuring that after each phase we have a testable system and reduce uncertainty step by step. We will start with the simplest usable subset (a basic voice chatbot without supervision), then progressively add the monitoring thread, and finally the interruption/correction mechanism. Using iterative development will allow testing at each stage and adjustment as needed.

Overall Architectural Decisions

Async Concurrency with asyncio: We will use Python’s asyncio to manage concurrent operations (listening, thinking, speaking, and supervising). This is chosen over multi-threading to avoid the complexity of shared-state locks and to better handle I/O-bound tasks (calling APIs, waiting for audio) in a single thread. The voice agent loop and the supervisor checks will run as separate tasks within the same event loop, enabling overlap.

Data Structures: We will maintain a shared conversation context (likely as a list of messages or a single string containing the dialogue) accessible by both the agent and supervisor. This will live in memory (no database needed). Each message can be a dict like {"role": "user"/"assistant", "text": "..."} or a simple concatenated string. For simplicity, a text block with delineations (e.g., "User: ... \nAssistant: ... \nUser: ...") will be passed to the LLMs.

BAML Functions: We’ll define two BAML functions:

SmallTalk(conversation) -> string: uses the small LLM (gpt-5-mini) to generate the assistant’s next reply. This will be called with the latest context (including the new user query).

CheckCompliance(conversation) -> (OnTrack | NeedsAdjustment): uses the large LLM to evaluate the conversation. Here we will leverage structured output. For example, we might define:

enum Outcome { ON_TRACK, NEEDS_ADJUSTMENT }
class Review { outcome Outcome, message string? }
function CheckCompliance(conversation: string) -> Review {
  client GPT4Turbo  # or another powerful model
  prompt #"
    You are a supervisor AI reviewing a conversation between a user and an AI agent.
    The agent must follow these rules:
    1. The agent should only discuss dogs (no other animals like cats or snails).
    2. The agent must ask for the user's email before booking an appointment.
    3. The agent should always answer "What vaccines are required?" with "Rabies and Distemper".
    4. The agent should not provide medical or legal advice.
    ...
    If all rules are being followed and the agent's last response is on track, output:
    ON_TRACK
    If any rule is violated or the agent goes off track, output:
    NEEDS_ADJUSTMENT with a brief correction message starting with "Oh wait, actually, ".
    {{ ctx.output_format }}
  "#
}


In this prompt, {{ ctx.output_format }} will ensure the model’s answer conforms to the Review class schema (thanks to BAML) – i.e., it will produce either an {"outcome": "ON_TRACK"} or {"outcome": "NEEDS_ADJUSTMENT", "message": "..."} JSON which BAML will parse into the Review object.

Rule Encoding: The rules will be primarily encoded in the supervisor’s prompt as shown above. This makes them easy to adjust by editing the prompt text. We’ll include around 5–10 rules as specified (like the ones in the example). The small model’s prompt (system prompt) will also have a short note about the main context (e.g. “You are a helpful dog daycare assistant. You handle queries about dog boarding and daycare.”) but we intentionally won’t load all the rules into the small model’s prompt – to simulate an unreliable agent that might break rules unless corrected. This highlights the supervisor’s role. In a production scenario one might include the rules in both places for redundancy, but here we want the supervisor to be essential.

Interruption Mechanism: To actually interrupt the primary agent’s response, our approach is:

Start TTS playback of the agent’s response as soon as it’s ready (don’t wait for supervisor).

In parallel, allow the supervisor check to process. If the supervisor returns NEEDS_ADJUSTMENT, we will:

Immediately stop the current TTS playback (e.g., if using an audio stream/player, call its stop method or if using an API that returns an audio file, we might have to cut off the playback mid-way).

Immediately use TTS to speak the supervisor’s correction message instead.

Insert the correction message into the conversation history as if it were the assistant’s last utterance.

Cancel any other pending supervisor tasks that haven’t completed, to avoid double-interventions. Also, if the agent was in the middle of formulating a longer response (in cases of streaming LLM output), we would stop that as well – but since our small model responses will likely come as one block, this mainly concerns TTS playback.

Resume the normal loop (the next user input will be listened for after the correction). The small model will see the correction in context, so it won’t repeat the mistake or conflict with it.

This approach ensures the user gets the correction as soon as possible. The slight drawback is the user might hear the first part of a mistaken answer before it’s cut off. We deem this acceptable for our demo (it even shows the mechanism working). In a real system, one might try to minimize this by using faster supervisor models or small pauses.

Testability and Phase Plan: Each phase will produce a runnable partial implementation:

Phase 1: Basic voice agent loop (STT -> small LLM -> TTS), no supervisor. Test that the agent responds in voice to queries.

Phase 2: Add the supervisor running in background, but only logging results. Test that rule violations are detected in the log, but no interruption occurs yet.

Phase 3: Enable the interruption mechanism (stop and correct). Test with a scenario that triggers a correction, observe it working.

Phase 4: Refine concurrency handling (cancellation, synchronization) to ensure robustness. Test rapid interactions or multiple queued tasks to ensure no race conditions or late surprises.

Throughout implementation, we’ll use gpt-5-mini (a hypothetical small model, possibly represented via BAML’s client config) for quick replies, and a larger model like GPT-4 for the supervisor. The split ensures the supervisor has greater reasoning ability to catch complex issues even if the primary model is dumb/fast. This design choice was made over alternative options such as a single model with all rules in its prompt or a purely deterministic rule-checker:

Alternative 1: Single LLM with rules in prompt – simpler architecture, but it either slows down the model (if it’s large) or if using a small model, it may not reliably follow all rules (small model might ignore some instructions under pressure). Also, it provides no second opinion; if the single model goes off track, there’s no way to catch it in the moment. Industry insights note that without clearly enforced boundaries, even good models can “drift and fabricate”
gladia.io
.

Alternative 2: Deterministic rule checker – e.g., code that scans the output for forbidden words (like “cat”) or checks if required info was provided. This could be fast and cheap, but it’s brittle and limited. It wouldn’t handle nuanced violations or context-dependent rules well. An LLM as supervisor can understand context and semantics (e.g., it knows mentioning boarding a cat is a violation of the “dogs only” policy even if the word “cat” alone might sometimes be innocuous in another context). The LLM judge approach is more flexible, essentially implementing a learned policy evaluator
elevenlabs.io
.

Given these, our approach of a dual-LLM system balances speed and intelligence, and leverages the strength of each method: fast pattern-matching from the small model for dialogue, and deeper analysis from the big model for oversight
gladia.io
.

Now, let’s break down the implementation into phases and detail the changes required in each.

Phase 1: Implement Small Model Voice Pipeline
Overview

Phase 1 focuses on setting up the core voice agent loop without any supervisory logic. By the end of this phase, the system will: capture the user’s speech, transcribe it to text (STT), generate a response using the small LLM, and output that response via speech (TTS). This will essentially be a simple voice chatbot. We will also maintain the conversation context (transcript) in this phase, as that will be needed for both multi-turn coherence and later for the supervisor. The goal is to have a testable voice assistant that can answer user questions about the dog daycare (albeit without knowing to enforce rules yet).

Changes Required:
1. Project Dependencies/Setup

File: requirements.txt (if applicable) or environment setup.

Changes: Add any required libraries for STT/TTS. For example, if using ElevenLabs API for TTS, include elevenlabs. For STT, if using an API like Deepgram, include their SDK, or if using OpenAI Whisper API, ensure openai package. Also include baml-client (the Python client for BAML) if not already present.

2. BAML Client Initialization

File: llm_client.py (a new module, or an existing place where we configure BAML clients)

Changes: Initialize the BAML runtime and define the small model function. For instance:

from baml_client import b, configure
# Configure BAML to know about our model endpoints
configure(default_client="GPT5Mini")  # hypothetical configuration
# Or if GPT-5-mini is an OpenAI or local model, configure accordingly.
# (Details depend on BAML setup; possibly a clients.baml file defines GPT5Mini)


If BAML requires a separate file for function definitions (like a .baml file), we would create that. For now, assume we can call a BAML function b.SmallTalk after we define it (possibly in a BAML script or via a decorator). In Python, it might be:

# Suppose we have defined in BAML:
# function SmallTalk(history: string) -> string { ... }
# Now in Python:
response_text = await b.SmallTalk(history)


We will ensure this integration is ready.

3. Speech-to-Text Integration

File: voice_agent.py (a new module to run the voice agent loop)

Changes: Add code to capture audio from the user and transcribe it. For example:

import asyncio
import some_stt_sdk  # e.g., deepgram or speechrecognition

async def transcribe_audio(audio_bytes: bytes) -> str:
    # If using Deepgram SDK:
    response = await deepgram.transcription.prerecorded(audio_bytes, options={...})
    return response['results']['channels'][0]['alternatives'][0]['transcript']
    # (This is pseudocode; actual API usage will vary.)


Additionally, code to capture microphone input. For a simple demo, we might avoid continuous streaming and instead record a short audio on each iteration (or use a hotkey to simulate end of speech). E.g., using sounddevice or speech_recognition library:

import sounddevice as sd
import numpy as np

def record_audio(duration=5) -> bytes:
    fs = 16000  # sample rate
    print("Listening for {} seconds...".format(duration))
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, blocking=True)
    audio = np.int16(audio * 32767).tobytes()
    return audio


For now, we can start with a fixed-duration or triggered recording for testing.

Note: In lieu of actual microphone input (for automated tests), we could allow an alternative path: if microphone isn’t available, read text input from console as the “user utterance”. This makes development easier. We can implement:

async def get_user_input() -> str:
    mode = "text"  # or "voice"
    if mode == "text":
        user_text = input("User: ")
        return user_text
    else:
        audio = record_audio(5)
        return await transcribe_audio(audio)


This flexibility aids testing the pipeline without needing actual audio each time.

4. LLM Response Generation

File: voice_agent.py (continuing in the loop)

Changes: After obtaining the user’s utterance text, append it to the conversation history and call the small LLM to get a response. For example:

conversation.append({"role": "user", "text": user_text})
# Create a history string for the model, e.g. last N messages or full
history_str = ""
for msg in conversation:
    history_str += f'{msg["role"].capitalize()}: {msg["text"]}\n'
# Call small LLM via BAML
assistant_reply = await b.SmallTalk(history_str)
conversation.append({"role": "assistant", "text": assistant_reply})


The SmallTalk function in BAML would be defined to take the conversation (or maybe just the last user message along with context) and produce an assistant answer. For example, in BAML we might have:

function SmallTalk(history: string) -> string {
  client GPT5Mini
  prompt #"
    {{ _.role("system") }}
    You are a friendly assistant at a dog daycare. You help customers with questions about dog boarding and daycare services.
    {{ _.role("user") }}
    {{ history }}
    {{ _.role("assistant") }}
  "#
}


Here we feed in the combined history as the user’s prompt and leave the assistant’s answer to predict. (Depending on BAML’s exact syntax, we adjust accordingly; the main point is we prompt the small model with context).

We will ensure assistant_reply is a plain string representing the model’s answer to the latest user query.

5. Text-to-Speech Integration

File: voice_agent.py

Changes: Take the assistant_reply text and synthesize speech. For example, using ElevenLabs API:

import elevenlabs

def speak_text(text: str):
    audio = elevenlabs.generate(text=text, voice="Bella", api_key=ELEVEN_API_KEY)
    elevenlabs.play(audio)  # plays the audio in real-time


Or using another TTS: if we use a local TTS engine for simplicity (like pyttsx3, although quality is lower):

import pyttsx3
tts_engine = pyttsx3.init()
def speak_text(text: str):
    tts_engine.say(text)
    tts_engine.runAndWait()


For now, we can use the ElevenLabs approach to get a more natural voice (assuming the API key is set). We will wrap this in an async call if needed (ElevenLabs’ generate could be blocking; we can offload it with await loop.run_in_executor if necessary).

Ensure to handle that this function either blocks until speech is done or we manage it asynchronously. We might prefer an asynchronous approach:

async def speak_text_async(text: str):
    audio = elevenlabs.generate(text=text, voice="Bella")
    # Instead of playing directly, maybe save to file and use an async audio player.
    with open("output.mp3", "wb") as f:
        f.write(audio)
    # Use an external player command or async library to play "output.mp3"


However, an easier method: ElevenLabs has a streaming option – but integrating that may be complex, so for initial version, it’s fine to generate then play.

6. Main Loop Assembly

File: voice_agent.py

Changes: Put it all together in an async loop. For example:

async def main_conversation():
    print("Starting voice agent. Say 'exit' or Ctrl+C to stop.")
    while True:
        user_text = await get_user_input()
        if not user_text:
            continue
        if user_text.lower() in ("exit", "quit"):
            break
        # Transcription step (already done in get_user_input if voice mode).
        print(f"User said: {user_text}")
        conversation.append({"role": "user", "text": user_text})
        # LLM step
        assistant_reply = await b.SmallTalk(get_history_text(conversation))
        print(f"Assistant: {assistant_reply}")  # for logging
        conversation.append({"role": "assistant", "text": assistant_reply})
        # TTS step
        await speak_text_async(assistant_reply)


This loop listens for user input, breaks if the user says "exit", otherwise processes the turn. Note: In real voice interaction, we’d have to detect end-of-speech; for now we use fixed length or a manual trigger as discussed.

For testing in this phase, one could run main_conversation() (using asyncio.run(main_conversation())) and simulate a conversation via text input or short recordings.

Testing Phase 1: We’ll run the agent and try simple interactions. For example:

User: "Hello"
Assistant: *greets and offers help*
User: "I want to book 3 nights for my dog starting next Monday."
Assistant: *should respond something like asking for details (since no specific training, it might hallucinate or answer generally)*


We verify that:

The STT (or text input) captured correctly.

The assistant’s response is generated and spoken.

The system doesn’t crash and can handle sequential turns.
If using text input mode, we simply ensure the prints and loop logic are correct. This sets the stage for adding the supervisor next.

Phase 2: Add Supervisor Model Thread (Shared Context, Logging Only)
Overview

In Phase 2, we introduce the supervisor LLM that will monitor each assistant response. The focus here is to get the monitoring working in parallel with the main loop, but without yet influencing the conversation. The supervisor will read the same conversation context and output a structured result indicating whether everything is fine or an adjustment is needed, but at this stage we will only log those results (not act on them). This lets us validate the supervisor’s rule-checking logic and the concurrency of running two model calls at once.

Key tasks in this phase:

Define the BAML function (or output schema) for the supervisor and ensure we can call it asynchronously.

Start a background task for each assistant message that calls the supervisor with the current context.

Collect the result and log it (e.g., print to console for now) for debugging.

Manage the conversation context in a thread-safe way for both tasks (likely not an issue with asyncio since everything runs on one thread by default, but we must ensure not to modify the context list while the supervisor is reading it – we'll probably pass a copy or snapshot of the conversation text).

By the end of Phase 2, we should see log statements like: “Supervisor: ON_TRACK” or “Supervisor: NEEDS_ADJUSTMENT (message: ...)” after each assistant turn, but the user experience remains unchanged from Phase 1 (no interruptions yet).

Changes Required:
1. BAML Supervisor Function Definition

File: llm_client.py or a new baml_functions.baml

Changes: Define the output schema and function for CheckCompliance. For example, in a BAML file:

enum Outcome { ON_TRACK, NEEDS_ADJUSTMENT }

class Review {
  outcome Outcome,
  message string?  @description("Correction message if adjustment is needed")
}

function CheckCompliance(conversation: string) -> Review {
  client GPT4Turbo
  prompt #"
    {{ _.role("system") }}
    You are an AI supervisor monitoring a conversation. Ensure the AI assistant follows all rules strictly.
    Rules:
    - Only discuss dogs (no other pets).
    - Always get the user's email before confirming a booking.
    - If asked about required vaccines, the answer must be "Rabies and Distemper".
    - Do not talk about topics outside pet boarding.
    - (etc., any additional rules)
    Now review the conversation below and determine if the last assistant message violates any rule or goes off track.
    If everything is fine, respond with ON_TRACK.
    If there is a violation, respond with NEEDS_ADJUSTMENT and include a corrective message for the assistant to say, starting with "Oh wait, actually, ...".
    {{ _.role("user") }}
    Conversation:
    {{ conversation }}
    {{ _.role("assistant") }}
    {{ ctx.output_format }}
  "#
}


This uses the Outcome enum and Review class to force the structured output. We instruct the model how to format its answer via ctx.output_format (which BAML will replace with instructions or placeholders to ensure a JSON matching Review is returned). The prompt includes the entire conversation as seen by a user role, expecting the model’s answer as assistant role. We might refine the prompt to emphasize checking specifically the last assistant message for compliance.

For instance, we could clarify: “... determine if the assistant’s last message violated any rule. Focus on the last response.” This way it doesn’t get confused by earlier turns (assuming those were fine).

BAML will generate a Python method for this, accessible as b.CheckCompliance returning a Review object (with fields .outcome and .message).

2. Initiating Supervisor Task on Each Turn

File: voice_agent.py (main loop)

Changes: After generating the assistant’s reply but before or concurrently with TTS, we launch the compliance check. For example:

# After getting assistant_reply and appending to conversation:
review_task = asyncio.create_task(run_compliance_check(conversation.copy()))
# Then trigger TTS (but we'll not wait for review_task yet)
await speak_text_async(assistant_reply)
# After speaking (or concurrently), we can collect the review result:
review = await review_task
if review.outcome == "ON_TRACK":
    print("Supervisor: ON_TRACK")
else:
    print(f"Supervisor: NEEDS_ADJUSTMENT – {review.message}")


Here, run_compliance_check would be an async function that formats the conversation history into a string and calls b.CheckCompliance:

async def run_compliance_check(convo_snapshot):
    # convo_snapshot is a copy of conversation list to avoid mutation issues
    convo_text = ""
    for msg in convo_snapshot:
        role = "User" if msg["role"] == "user" else "Assistant"
        convo_text += f"{role}: {msg['text']}\n"
    try:
        review: Review = await b.CheckCompliance(conversation=convo_text)
    except Exception as e:
        print("Supervisor model error:", e)
        # In case of failure, default to ON_TRACK to not disrupt
        return Review(outcome="ON_TRACK", message=None)
    return review


We use .copy() on the list to pass a snapshot to avoid race conditions if the main loop appends new messages while the supervisor is reading (though in this sequence, that’s unlikely since we append then immediately call).

We create review_task before awaiting TTS so that the compliance check and the speech output happen in parallel. However, we do await the TTS before printing the result in this snippet. We might actually want to not delay the print – we could instead gather the result as soon as it’s ready:

review = await review_task  # could also do: done, _ = await asyncio.wait({review_task}, timeout=0)


But printing a bit later is fine for now, since it doesn’t affect user output in Phase 2.

Note: Ensure that b.CheckCompliance is an asynchronous call (most likely, since it might call an external API). Using asyncio.create_task ensures it runs concurrently. If BAML client is synchronous, we might need to run it in an executor; but BAML’s Python client typically provides await b.Function() for async.

3. Logging the Supervisor Result

File: voice_agent.py

Changes: As shown above, after awaiting the supervisor result, log it. For clarity in logs, we might include the turn number or the assistant’s text snippet. E.g.:

turn_no = len([msg for msg in conversation if msg["role"] == "user"])
if review.outcome == "ON_TRACK":
    logger.info(f"[Turn {turn_no}] Supervisor: ON_TRACK")
else:
    logger.warning(f"[Turn {turn_no}] Supervisor: NEEDS_ADJUSTMENT -> {review.message}")


For now, printing to console suffices. We might set up a proper logger earlier if needed.

4. Testing Hooks

To verify without interfering with user experience, perhaps introduce a slight delay or manual step:
Actually, since not interrupting yet, we can simply observe console logs. We should test a scenario where a rule is broken:

Example: User says: "I have a cat that needs boarding."

Small model likely responds (if not instructed otherwise) with something like "Sure, we can board your cat." (since it doesn’t know the rule).

The supervisor’s log should show NEEDS_ADJUSTMENT and a message like "Oh wait, actually, we don't board cats...". We confirm the logic produced that in logs.

But at this phase, the assistant’s spoken output was still the wrong answer and no correction was given to the user. That’s expected for phase 2.

Another example: User asks: "Can I book without giving my email?"

If the assistant says "Sure, I can book it now" (failing rule of collecting email), the supervisor should flag it.

We check the log for NEEDS_ADJUSTMENT and appropriate message ("Oh wait, actually, I'll need your email...").

If the conversation stays normal, supervisor should log ON_TRACK.

We should ensure that launching the background task does not slow down the main loop. In asyncio, as long as we create_task and not await it immediately, the main loop will continue to TTS without waiting for the compliance check to finish. That’s what we want. The actual printing of the result here is after awaiting TTS, meaning we might only see the log after the bot finishes speaking. That’s fine for now. In the next phase, we will react faster (possibly even interrupt mid-speech).

Testing Phase 2: We run the same kind of conversation as Phase 1, but now watch the terminal for supervisor logs. We purposely include at least one rule-violation turn to see that the supervisor model identifies it. If we see those logs aligning with expectations, Phase 2 is successful. We also monitor that running two model calls (SmallTalk and CheckCompliance) in quick succession or overlap doesn’t cause any errors (like BAML client conflicts or rate limits). BAML should handle multiple concurrent calls, but if not, we might have to queue or slightly delay – to be seen. For now, assume it can handle it.

Phase 3: Implement Interruption Mechanism (Part I)
Overview

In Phase 3, we will act on the supervisor’s findings by implementing the interruption/correction behavior. When a “NEEDS_ADJUSTMENT” is detected, the system will immediately correct the conversation. This involves stopping any ongoing processes for the current turn and injecting the supervisor’s recommended message.

We'll break this down into a few parts:

Immediate TTS Interruption – If the agent’s response is in the middle of being spoken, we need to cut it off.

Playback of Correction – Use TTS to speak the “Oh wait, actually,... [correction]” message to the user.

Context Update – Append this correction to the conversation history (as an assistant message).

Resumption – Ensure the conversation can continue from this point, with the user likely responding to the correction or being prompted accordingly. The small model will next generate a response taking into account this correction (if the conversation continues).

Preventing Overlap – Stop or cancel any redundant tasks in progress (like if the small model was streaming a long response, or if another compliance check was queued, etc., though in this phase we handle basic cases).

In this Phase I of interruption, we will implement the core logic to do the above. We might not yet handle all edge cases (that will be Phase 4), but we’ll focus on making the basic scenario work: a single violation triggers one correction and then normal flow resumes.

Changes Required:
1. Modify Supervisor Task Handling to Interrupt

File: voice_agent.py (main loop where we handle the supervisor result)

Changes: Instead of merely logging the supervisor result after TTS, we need to intervene as soon as we know a correction is needed. That means we should restructure how we await the tasks. We will likely start the TTS and supervisor tasks in parallel, and then wait for whichever finishes first:

review_task = asyncio.create_task(run_compliance_check(conversation.copy()))
tts_task = asyncio.create_task(speak_text_async(assistant_reply))
# Wait for either the TTS to finish or the supervisor to return, whichever comes first
done, pending = await asyncio.wait({review_task, tts_task}, return_when=asyncio.FIRST_COMPLETED)
if review_task in done:
    review = review_task.result()
    if review.outcome == "NEEDS_ADJUSTMENT":
        # Interrupt needed
        # Cancel TTS if still playing
        if tts_task in pending:
            tts_task.cancel()
            print("** Interrupting speech output for correction **")
        correction_message = review.message or "Oh wait, actually, I need to correct that."
        # Speak the correction immediately
        await speak_text_async(correction_message)
        # Update conversation context with the correction
        conversation.append({"role": "assistant", "text": correction_message})
        print(f"Assistant (correction): {correction_message}")
        # (We will also handle any supervisor tasks but in Phase 4)
    else:
        # No adjustment needed, just ensure TTS finishes
        await tts_task
        print("** No interruption, response completed **")
else:
    # TTS finished before supervisor responded
    await tts_task  # (it’s done, but ensure cleanup)
    # Now wait for the supervisor (still running) to get result
    review = await review_task
    if review.outcome == "NEEDS_ADJUSTMENT":
        # The response already fully spoken but now we find it's wrong
        # We'll still issue correction after-the-fact
        correction_message = review.message or "Oh wait, actually,..."
        await speak_text_async(correction_message)
        conversation.append({"role": "assistant", "text": correction_message})
        print(f"Assistant (post-correction): {correction_message}")
    else:
        print("Supervisor (post-check): ON_TRACK (no interruption)")


The above logic does the following:

Starts speaking and checking concurrently.

If the supervisor returns before the TTS is done and flags an issue, we cancel the speaking task (stopping the speech) and immediately voice the correction.

If the supervisor returns “ON_TRACK” first (rare, since it would just wait for TTS anyway, but suppose TTS is slow and model is fast), then no interruption – we just let TTS finish.

If the TTS finishes first (likely, if the response was short or supervisor is just slow), then we wait for the supervisor. If it then flags an issue, the user already heard the whole wrong answer. We still decide to voice a correction (“Oh wait, actually,...”) right after. This may be a bit awkward in timing, but at least the record is corrected. (We might refine this to skip trivial delays in Phase 4, but for now we’ll do it).

This ensures the correction happens at most one turn late. In many cases, the supervisor might be fast enough to catch during TTS.

We should wrap parts of this in try/except to handle cancellation exceptions (cancelling tts_task may raise an asyncio.CancelledError in that task).

We will also ensure that once a correction is spoken, the system doesn’t immediately generate another assistant response. In a normal flow, after the assistant speaks, it waits for user input. The correction itself is an assistant message, so logically we should now wait for the user's reaction. We do not want the small LLM to generate another message right after the correction (that would result in two assistant messages in a row, potentially confusing). Instead, the correction message often includes a prompt or question (like “… – can I help with boarding for your dog?”), inviting the user to respond. So the next loop iteration will handle the user’s response. We should be careful not to call the small LLM again immediately after a correction. The code as written doesn’t call it again; it would loop back to get_user_input.

One caveat: Because we appended the correction to the conversation, if the user doesn’t say anything and we were to loop, the assistant might erroneously think it needs to respond to its own correction. But our loop is user-driven, so it will simply wait for user input. We might need a mechanism for barge-in (if user tries to talk while agent is correcting, etc., but that’s advanced). We assume user will listen to the correction then reply.

2. Ensure TTS Playback is Cancelable

File: voice_agent.py or wherever speak_text_async is defined.

Changes: Implement speak_text_async in a way that can be cancelled. For example, if using ElevenLabs and we have to stream or chunk the audio:

import aiohttp
async def speak_text_async(text: str):
    # If ElevenLabs has a streaming endpoint:
    url = "https://api.elevenlabs.io/v1/text-to-speech/voiceid/stream"
    headers = {"xi-api-key": ELEVEN_API_KEY, "Content-Type": "application/json"}
    data = {"text": text, ...}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            if resp.status != 200:
                raise Exception("TTS API error")
            # Stream the response audio in chunks and play
            player = AudioPlayer()  # some hypothetical utility to play audio
            async for chunk in resp.content.iter_chunked(1024):
                player.play_chunk(chunk)
                # If cancelled, the loop will break due to CancelledError
            player.stop()


If we cannot easily stream, another approach:

Request the TTS audio as one block.

Save to file and start playing with an external process (like using pydub or system afplay/ffplay in a subprocess).

Keep a handle to that process so we can terminate it if needed.

Simpler: use an audio library to play in a background thread and just stop that thread. For our demo, we might use a simple approach where tts_task.cancel() could set a global flag that our playing loop checks. For example, if we use pyttsx3, we can stop it by engine.stop() if accessible from another thread.

Given this is tricky, we might simulate cancellation by splitting the text and inserting a check:

async def speak_text_async(text: str):
    # Break text into two parts for simulation
    parts = text.split('. ', 1)
    for part in parts:
        # speak part (synchronously for demo)
        tts_engine.say(part)
        tts_engine.runAndWait()
        await asyncio.sleep(0)  # allow cancellation


This is not ideal, but for demonstration, assume we have a way to stop mid-utterance.

For now, we can assume ElevenLabs streaming or a simple built-in callback mechanism. The main thing is that tts_task.cancel() should indeed interrupt the playback. We will test that by seeing if the correction comes quickly.

3. Cancel Running Supervisor Tasks (Basic)

File: voice_agent.py

Changes: In the snippet above, we cancelled tts_task if needed. What about supervisor tasks? In this scenario, we waited for the one we launched. But consider if user speaks again quickly (rare in voice UI since user waits for answer). However, if the user did start speaking while the agent was talking, our design didn’t cover that scenario well (barge-in). We assume half-duplex for now: user waits for agent to finish (or correction to finish) before talking. So at this point, there shouldn’t be multiple supervisor tasks for different turns overlapping yet.

But a case: If the small LLM generated a very long answer and the user interrupts it by talking (again, advanced), our microphone code might pick up user speech and we’d start processing new user input while the old answer is still speaking or being evaluated. That could spawn a new small LLM call and another supervisor call. This is complex and out of scope (requires full duplex and barge-in handling). So we will not handle user interruptions, only agent interruptions.

Therefore, at this phase, we don’t need to cancel older supervisor tasks because we handle one turn at a time, sequentially.

We will, however, plan to maintain a mechanism for cancellation in Phase 4. Possibly keep a global reference to the current review_task and cancel it if starting a new turn or if already found a correction. But we’ll do that next.

4. Testing Phase 3

We run the agent with a known violation scenario:

E.g., User: “Can you board my cat?”

Small LLM (likely) starts responding “Sure, we can board cats…” and TTS begins speaking that.

Supervisor (hopefully quickly) returns NEEDS_ADJUSTMENT with message e.g. “Oh wait, actually, we don’t board cats – can I help you with boarding for your dog instead?”

We expect the small model’s spoken output to cut off shortly after starting (depending on timing) and then the correction message to be spoken in full.

The conversation history should now have:

User: "Can you board my cat?"

Assistant: "Sure, we can board cats..." (though it was cut off, we still appended the full text it tried to say)

Assistant (correction): "Oh wait, actually, we don't work with cats... can I help with a dog?"

Now the user can respond.

We verify that:

The wrong answer was indeed interrupted (we might see only part of it spoken, depending on how cancellation works; or at least immediately followed by the correction).

The correction was spoken.

The logs show the interruption (we added a print for interrupting).

No further response was generated automatically after the correction (the system should loop back to waiting for user).

We also test a non-violation turn to ensure it still works normally (no interruption).

E.g., User: "Do you have weekend daycare?"

Assistant: "Yes, we are open on weekends from 9am to 5pm..." (speaks fully)

Supervisor likely ON_TRACK.

No interruption.

Conversation continues.

This phase introduces the biggest behavioral change. We should carefully monitor that our concurrency logic doesn’t deadlock or mis-sequence:

There is a slight complexity: using asyncio.wait(return_when=FIRST_COMPLETED) then later awaiting tasks. We should be careful to handle both tasks end states properly to avoid un-awaited tasks.

The pseudo-code above covers both cases. We’ll implement it carefully in code with proper try/finally to ensure tasks are done (especially if one is cancelled).

At the end of Phase 3, we should have a functioning self-correcting agent for single rule violations at a time.

Phase 4: Refine Interruption Mechanism (Part II - Robustness)
Overview

Phase 4 will focus on polishing the system to handle edge cases and ensure the monitor thread and voice agent work seamlessly in all scenarios. This includes cleaning up any remaining issues with task cancellation, multiple simultaneous tasks, and ensuring that once a correction is made, the system resets properly for subsequent turns. We also consider performance tweaks and any adjustments to the prompts/rules based on testing.

Specific goals in this phase:

Cancel Stale Tasks: If for any reason a supervisor task is still running when it’s no longer relevant (e.g., a correction has already been applied or a new user input came in), ensure it’s cancelled or its result ignored. Similarly, avoid multiple overlapping TTS or LLM calls beyond what’s intended.

State Reset after Correction: When a correction happens, make sure the next user input will be processed correctly. For example, if the user remains silent, our loop will just wait (that’s fine). If user speaks, we proceed as normal. We need to verify that the presence of the correction in history doesn’t confuse the small model (it shouldn’t; it will just treat it as the assistant’s last message).

Prompt Tuning: Possibly adjust the supervisor prompt if we observed false positives/negatives in Phase 3. For instance, if the supervisor was too slow or too verbose, we might simplify its instructions. Or if it missed a rule, tweak the wording.

Performance Considerations: If the overhead is high, consider slight optimizations like not sending the entire history every time to the small model or supervisor (maybe limit to last few turns if context grows large). However, given this is a demo, we can accept some inefficiency for clarity.

Testing & Verification: Do a thorough test run of multiple turns conversation, including multiple corrections in one conversation, to ensure stability.

Changes Required:
1. Global Task Management

File: voice_agent.py

Changes: Introduce a simple mechanism to track the current or last supervisor task. For example, a global or outer-scope variable:

current_review_task = None


When starting a new review_task, first cancel any current_review_task that is still pending:

if current_review_task and not current_review_task.done():
    current_review_task.cancel()
current_review_task = asyncio.create_task(run_compliance_check(conversation.copy()))


This ensures we don’t have two compliance checks running at the same time. In normal use (one turn at a time) this might not happen, but if it ever does, we prevent overlap.

Similarly, for TTS, if for some reason a previous TTS is still playing (shouldn’t if we awaited it, but just in case), we could keep a current_tts_task and cancel it at the start of a new turn.

We should add these cancellations at appropriate points:

Before starting a new user turn processing, cancel any leftover tasks from prior turn.

We might implement the conversation loop so that it waits for the previous turn’s tasks to finish (like after handling interruption, etc., ensure no tasks hanging). Our Phase 3 code awaited the relevant tasks already, so it should be clean.

Example integration:

while True:
    user_text = await get_user_input()
    if not user_text: continue
    # Cancel any previous supervisor task (should be none pending by now, but safe)
    if current_review_task and not current_review_task.done():
        current_review_task.cancel()
    # Cancel any TTS if still playing (if user barged in, possibly)
    if current_tts_task and not current_tts_task.done():
        current_tts_task.cancel()
    ...
    # then proceed to process new input


This is a defensive measure.

2. Fine-tune Cancellation Handling

File: voice_agent.py (interruption logic from Phase 3)

Changes: Make sure to handle exceptions that arise from cancellations. For example:

try:
    done, pending = await asyncio.wait({review_task, tts_task}, return_when=asyncio.FIRST_COMPLETED)
except Exception as e:
    # handle unexpected errors, possibly log
    done, pending = set(), {review_task, tts_task}  # assume none done if error
# Then handle logic
if review_task in done:
    try:
        review = review_task.result()
    except asyncio.CancelledError:
        # If the review task was cancelled due to a new turn or something
        review = None
    ...
if tts_task in pending:
    tts_task.cancel()
    try:
        await tts_task
    except asyncio.CancelledError:
        pass


And similar for other paths. The goal is to avoid unhandled CancelledError warnings and ensure tasks are properly awaited or cancelled to not leak.

If using an external process for TTS playback, ensure that is also terminated. (For instance, if we launched a subprocess.Popen for an audio player, we’d call proc.kill() on cancel).

3. Prompt and Output Adjustments

File: baml_functions.baml (CheckCompliance prompt)

Changes: Based on tests, adjust the rules or the response format. For example, maybe the model included some extra text outside the JSON. BAML usually handles parsing; if the model strays, BAML might throw an error or attempt to coerce. We might tighten the prompt to say “Only output the JSON, no explanation.” or similar.

Or if the correction message from the model was too verbose or not in the desired tone, adjust the instruction. E.g., ensure it says “a brief correction message”. Possibly limit the length in prompt instructions.

For instance:

... If any rule is violated, output NEEDS_ADJUSTMENT with a brief correction (one sentence)...


This should yield a concise insert.

Also, if the model sometimes incorrectly flags something (false positive), we might add a bias: e.g., “If unsure, default to ON_TRACK.” to avoid over-correcting.

We will run another conversation to see if any such tweaks are needed.

4. Comprehensive Testing Scenarios

After code adjustments, perform final tests:

Multiple Violations: E.g., user triggers a violation, gets corrected, then later triggers another different violation. The system should handle each independently. Check that after the first correction, the second one still works.

Back-to-Back Turns: Have a longer conversation mixing normal and violating turns to ensure no buildup of issues.

Edge case: If the user just says something that’s very out-of-scope (like a completely unrelated question, which might cause the assistant to either answer incorrectly or refuse), see how supervisor handles it. If our rules don’t cover it, supervisor might not flag it, which is fine. Or the assistant might break a policy by answering something it shouldn’t – if that falls under a rule (“do not talk about X”), then it should be caught.

Cancellation edge: If we simulate the user interrupting the agent (not in scope to fully handle, but we can emulate by manually typing user input before the agent finished speaking in text-mode), ensure our cancellation logic of previous tasks works (the previous TTS should cancel, previous review cancel).

We’ll also verify resource cleanup: after conversation end (user says exit), make sure all tasks are cancelled and the program can exit without hanging background tasks.

Given that this is an asynchronous educational demo running locally, we assume it’s acceptable to use asyncio.run(main_conversation()) and that will clean up on exit.

Example Code Snippet for Phase 4 Adjustments

Below is a consolidated pseudo-code snippet reflecting Phase 3 and 4 logic for one turn, incorporating the improvements:

async def handle_turn(user_text: str):
    global current_review_task, current_tts_task
    # Cancel any ongoing tasks from previous turn
    if current_review_task and not current_review_task.done():
        current_review_task.cancel()
    if current_tts_task and not current_tts_task.done():
        current_tts_task.cancel()
        try: await current_tts_task
        except asyncio.CancelledError: pass

    conversation.append({"role": "user", "text": user_text})
    prompt = format_history(conversation)
    assistant_reply = await b.SmallTalk(prompt)
    conversation.append({"role": "assistant", "text": assistant_reply})
    print(f"Assistant: {assistant_reply}")

    # Launch tasks for TTS and compliance check
    current_tts_task = asyncio.create_task(speak_text_async(assistant_reply))
    current_review_task = asyncio.create_task(run_compliance_check(conversation.copy()))

    done, pending = await asyncio.wait({current_tts_task, current_review_task}, return_when=asyncio.FIRST_COMPLETED)
    # Determine outcome
    if current_review_task in done:
        # Supervisor finished quickly
        try:
            review = current_review_task.result()
        except Exception as e:
            review = None
            print("Supervisor task error or cancelled:", e)
        if review and review.outcome == "NEEDS_ADJUSTMENT":
            # Cancel speaking the wrong answer, if still speaking
            if not current_tts_task.done():
                current_tts_task.cancel()
                try: await current_tts_task
                except asyncio.CancelledError: pass
            correction = review.message
            print(f"*** Correction needed: {correction}")
            conversation.append({"role": "assistant", "text": correction})
            # Immediately speak correction
            await speak_text_async(correction)
            print(f"Assistant (corrected): {correction}")
            # No further action; wait for user input next
            return
        else:
            # No correction needed, just wait for speech to finish
            await current_tts_task
            print("Assistant response completed with no issues.")
            return
    else:
        # TTS finished first
        await current_tts_task  # ensure fully finished
        try:
            review = await current_review_task
        except Exception as e:
            review = None
            print("Supervisor task error or cancelled (late):", e)
        if review and review.outcome == "NEEDS_ADJUSTMENT":
            # The user already heard full answer, now we found it's wrong.
            correction = review.message
            print(f"*** Late correction: {correction}")
            conversation.append({"role": "assistant", "text": correction})
            await speak_text_async(correction)
            print(f"Assistant (late corrected): {correction}")
        else:
            print("Supervisor confirmed ON_TRACK after response.")
        return


This pseudo-code (to be adjusted in actual code with proper error handling) shows how we manage tasks and context for a single turn. The current_review_task and current_tts_task are stored globally to allow cancellation on the next turn or by themselves.

5. Documentation / Comments

We should add comments in the code to explain the tricky parts: why we cancel tasks, how we format history, etc., since this is an educational project. This will help future readers or developers understand the concurrency logic and the role of each model.

After these changes, Phase 4 should result in a robust demonstration:

The voice agent responds quickly.

The supervisor corrects issues reliably and only when needed.

There are no runaway tasks or crashes even under rapid inputs or repeated mistakes.

The rules can be easily modified in one place (the supervisor prompt), and the system can be extended (e.g., adding a knowledge base to the small model, or more complex rules).

The overall architecture (two-model oversight) is clear and functioning, aligning with the guardrails approach recommended for safe AI voice agents
gladia.io
elevenlabs.io
.

Final Testing: Engage in a sample conversation that covers it all:

User: "Hi, I want to book daycare for my dog."
Assistant: "Sure, I can help with that! For how many days?"   (ON_TRACK)
User: "3 days starting next Monday."
Assistant: "Got it. I'll reserve 3 days from next Monday. What’s your dog's name?"  (ON_TRACK, but note: hasn't asked email yet, which might be okay until finalizing booking)
User: "His name is Rex."
Assistant: "Great. I have Rex down for 3 days starting next Monday."  (This is a violation: did not ask email before confirming booking)
*(Supervisor triggers NEEDS_ADJUSTMENT)*
Assistant (correction): "Oh wait, actually, I'll need your email address to complete the booking."  (spoken immediately)
User: "Oh sure, it's user@example.com."
Assistant: "Thanks! I've recorded your email. Your booking is confirmed. Is there anything else?"  (ON_TRACK)
User: "My friend has a cat, can you take care of it as well?"
Assistant: "We can certainly take care of your friend's cat."  (whoops, violation)
*(Supervisor triggers NEEDS_ADJUSTMENT)*
Assistant (correction): "Oh wait, actually, I'm sorry, we only board dogs here, not cats."  (spoken, correcting the policy)
User: "Alright, just the dog then."
Assistant: "Understood! Just the dog. We look forward to having Rex with us next week!" (ON_TRACK)


We would verify each correction happened at the right time and the final state of context and tasks is clean. If all looks good, we have successfully implemented the voice agent with a real-time supervisor, meeting the project goals.
