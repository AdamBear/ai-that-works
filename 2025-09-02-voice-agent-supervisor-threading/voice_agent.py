import asyncio
import os
import sys
from typing import Dict, List, Optional, Any
import logging
from dotenv import load_dotenv
from colorama import init, Fore, Style
import io
import wave
import threading
import queue
import time

# Initialize colorama for cross-platform color support
init(autoreset=True)
import sounddevice as sd
import numpy as np
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from openai import OpenAI
import tempfile
import subprocess
from baml_client.sync_client import b as b_sync
from baml_client.async_client import b

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)
logger = logging.getLogger(__name__)

# Configuration
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
CHANNELS = int(os.getenv("AUDIO_CHANNELS", "1"))

# Global state
conversation: List[Dict[str, str]] = []
tts_player_process: Optional[subprocess.Popen] = None
tts_stop_event = threading.Event()

# Initialize clients
elevenlabs_client = None
if ELEVENLABS_API_KEY:
    elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

def format_conversation(conv: List[Dict[str, str]]) -> str:
    """Format conversation history for LLM input."""
    result = []
    for msg in conv:
        role = "Customer" if msg["role"] == "user" else "Tony"
        result.append(f"{role}: {msg['text']}")
    return "\n".join(result)

def record_audio_with_silence_detection(max_duration: int = 10, silence_threshold: float = 0.01, silence_duration: float = 4.0) -> bytes:
    """Record audio with automatic silence detection."""
    logger.info(f"🎤 Listening (speak now, will stop after {silence_duration}s of silence)...")
    
    audio_queue = queue.Queue()
    recording = []
    silence_counter = 0
    silence_samples = int(silence_duration * SAMPLE_RATE)
    is_recording = False
    
    def audio_callback(indata, frames, time_info, status):
        """Callback for audio input."""
        if status:
            logger.warning(f"Audio status: {status}")
        audio_queue.put(indata.copy())
    
    # Start recording
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback):
        start_time = time.time()
        
        while time.time() - start_time < max_duration:
            try:
                data = audio_queue.get(timeout=0.1)
                recording.append(data)
                
                # Check for silence
                volume = np.abs(data).mean()
                
                if volume < silence_threshold:
                    if is_recording:  # Only count silence after speech started
                        silence_counter += len(data)
                        if silence_counter >= silence_samples:
                            logger.info("🔇 Silence detected, stopping...")
                            break
                else:
                    is_recording = True
                    silence_counter = 0
                    
            except queue.Empty:
                continue
    
    if not recording:
        return b''
    
    # Convert to bytes
    audio_data = np.concatenate(recording, axis=0)
    audio_bytes = np.int16(audio_data * 32767).tobytes()
    return audio_bytes

async def record_audio(duration: int = 5) -> bytes:
    """Record audio from microphone (async wrapper)."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, record_audio_with_silence_detection, duration)

async def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe audio to text using OpenAI Whisper API."""
    if not openai_client:
        logger.warning("OpenAI client not configured - using placeholder")
        return "Hello, I'd like to book daycare for my dog"
    
    if len(audio_bytes) == 0:
        return ""
    
    try:
        # Create WAV file in memory
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(CHANNELS)
            wav_file.setsampwidth(2)  # 16-bit audio
            wav_file.setframerate(SAMPLE_RATE)
            wav_file.writeframes(audio_bytes)
        
        wav_buffer.seek(0)
        wav_buffer.name = "audio.wav"
        
        # Transcribe using Whisper
        loop = asyncio.get_event_loop()
        transcription = await loop.run_in_executor(
            None,
            lambda: openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=wav_buffer,
                language="en"
            )
        )
        
        return transcription.text.strip()
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return ""

async def get_user_input() -> str:
    """Get user input via text or voice."""
    if DEMO_MODE:
        # Text input mode
        user_text = input(f"\n{Fore.GREEN}User: {Style.RESET_ALL}")
        return user_text
    else:
        # Voice input mode
        audio = await record_audio(5)
        user_text = await transcribe_audio(audio)
        # Print the transcribed text so user knows what was heard
        if user_text:
            print(f"\n{Fore.GREEN}User: {user_text}{Style.RESET_ALL}")
        return user_text

async def speak_text_async(text: str) -> None:
    """Convert text to speech and play it (cancellable)."""
    global tts_player_process, tts_stop_event
    
    tts_stop_event.clear()

    if not elevenlabs_client:
        # Fallback: simulate speaking time
        for _ in range(5):
            if tts_stop_event.is_set():
                return
            await asyncio.sleep(0.1)
        return

    try:
        # Generate audio from ElevenLabs
        loop = asyncio.get_event_loop()
        
        def generate_audio():
            return list(elevenlabs_client.generate(
                text=text,
                voice=ELEVENLABS_VOICE_ID,
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.0,
                    use_speaker_boost=True
                ),
                model="eleven_monolingual_v1"
            ))
        
        # Generate audio in executor to not block
        audio_chunks = await loop.run_in_executor(None, generate_audio)
        
        if tts_stop_event.is_set():
            return

        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            for chunk in audio_chunks:
                if tts_stop_event.is_set():
                    temp_file.close()
                    os.unlink(temp_file.name)
                    return
                temp_file.write(chunk)
            temp_path = temp_file.name

        if tts_stop_event.is_set():
            os.unlink(temp_path)
            return

        # Play audio using system player
        if sys.platform == "darwin":  # macOS
            tts_player_process = subprocess.Popen(["afplay", temp_path])
        else:  # Linux/Windows
            tts_player_process = subprocess.Popen(["ffplay", "-nodisp", "-autoexit", temp_path])

        # Wait for playback with cancellation check
        while tts_player_process.poll() is None:
            if tts_stop_event.is_set():
                stop_tts()
                break
            await asyncio.sleep(0.1)

        # Clean up
        try:
            os.unlink(temp_path)
        except:
            pass
        tts_player_process = None

    except Exception as e:
        logger.error(f"TTS error: {e}")
        await asyncio.sleep(0.5)

def stop_tts():
    """Stop any currently playing TTS audio."""
    global tts_player_process, tts_stop_event
    
    tts_stop_event.set()
    
    if tts_player_process and tts_player_process.poll() is None:
        tts_player_process.terminate()
        try:
            tts_player_process.wait(timeout=0.5)
        except subprocess.TimeoutExpired:
            tts_player_process.kill()
        tts_player_process = None

async def run_compliance_check(convo_snapshot: List[Dict[str, str]]) -> Any:
    """Run supervisor compliance check on conversation."""
    convo_text = format_conversation(convo_snapshot)
    try:
        review = await b.CheckCompliance(conversation=convo_text)
        return review
    except Exception as e:
        logger.error(f"Supervisor error: {e}")
        # Default to ON_TRACK on error to not disrupt
        return type('Review', (), {'status': 'ON_TRACK', 'message': None})()


async def stream_assistant_response(convo_text: str):
    """Stream the assistant's response."""
    try:
        stream = b.stream.SmallTalk(conversation=convo_text)
        return stream
    except Exception as e:
        logger.error(f"Streaming error: {e}")
        raise

async def handle_supervisor_result(supervisor_task: asyncio.Task, convo_snapshot: List[Dict[str, str]]) -> None:
    """Handle supervisor result asynchronously - completely non-blocking."""
    try:
        review = await supervisor_task
        if review and hasattr(review, 'status'):
            if review.status == "NEEDS_ADJUSTMENT":
                # Late correction - user is likely already typing
                print(f"\n{Fore.RED}Supervisor: ⚠️ NEEDS_ADJUSTMENT (late){Style.RESET_ALL}")
                if review.message:
                    print(f"{Style.DIM}Supervisor: {review.message}{Style.RESET_ALL}")
                    print(f"\n{Fore.YELLOW}Assistant: {review.message}{Style.RESET_ALL}")
                    # Speak the late correction
                    await speak_text_async(review.message)
            else:
                print(f"\n{Fore.CYAN}Supervisor: ✅ ON_TRACK{Style.RESET_ALL}")
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logger.debug(f"Supervisor task error: {e}")

async def handle_turn(user_text: str) -> None:
    """Handle a single conversation turn with real-time supervisor monitoring."""
    global conversation

    # Add user message to conversation
    conversation.append({"role": "user", "text": user_text})

    # Prepare conversation context
    convo_text = format_conversation(conversation)
    assistant_reply = ""
    interrupted = False
    tts_task = None
    
    print(f"\n{Fore.YELLOW}Assistant: {Style.RESET_ALL}", end="", flush=True)
    
    # Create streaming task
    stream_task = asyncio.create_task(stream_assistant_response(convo_text))
    
    # Create supervisor task that runs in parallel
    convo_snapshot = conversation.copy()
    supervisor_task = asyncio.create_task(run_compliance_check(convo_snapshot))
    
    try:
        # Stream the response while checking compliance in parallel
        stream = await stream_task
        
        async for partial in stream:
            # Check if supervisor has detected an issue DURING streaming
            if supervisor_task.done():
                review = await supervisor_task
                if review and hasattr(review, 'status') and review.status == "NEEDS_ADJUSTMENT":
                    # INTERRUPT IMMEDIATELY
                    stop_tts()  # Stop any ongoing TTS
                    print(f"\n\n{Fore.RED}Supervisor: ⚠️ NEEDS_ADJUSTMENT{Style.RESET_ALL}")
                    if review.message:
                        print(f"{Style.DIM}Supervisor: {review.message}{Style.RESET_ALL}")
                    
                    # Cancel the stream
                    interrupted = True
                    
                    # Use supervisor's correction
                    correction = review.message or "Actually, let me correct that..."
                    print(f"\n{Fore.YELLOW}Assistant: {correction}{Style.RESET_ALL}")
                    
                    # Speak the correction immediately
                    await speak_text_async(correction)
                    
                    # Update conversation with correction
                    assistant_reply = correction
                    break
            
            # Continue streaming if not interrupted
            if partial and not interrupted:
                new_text = partial[len(assistant_reply):] if len(partial) > len(assistant_reply) else ""
                if new_text:
                    print(f"{Fore.YELLOW}{new_text}{Style.RESET_ALL}", end="", flush=True)
                    assistant_reply = partial
        
        if not interrupted:
            # Get final response if not interrupted
            assistant_reply = await stream.get_final_response()
            print()  # New line after streaming
            
            # CRITICAL: Fire-and-forget supervisor handling
            # This runs in background while user can already type
            if not supervisor_task.done():
                asyncio.create_task(handle_supervisor_result(supervisor_task, convo_snapshot))
            else:
                # Supervisor finished during streaming - show result
                review = await supervisor_task
                if review and hasattr(review, 'status'):
                    if review.status == "ON_TRACK":
                        print(f"\n{Fore.CYAN}Supervisor: ✅ ON_TRACK{Style.RESET_ALL}")
        
    except Exception as e:
        logger.error(f"Error in handle_turn: {e}")
        assistant_reply = "I'm sorry, I'm having trouble processing that request."
        print(f"\n{Fore.YELLOW}{assistant_reply}{Style.RESET_ALL}")
    finally:
        # Cancel stream task if needed
        if not stream_task.done():
            stream_task.cancel()
        # DO NOT cancel supervisor - let it run in background

    # Add final response to conversation
    conversation.append({"role": "assistant", "text": assistant_reply})
    
    # Speak the final response (if not already interrupted and spoken)
    if assistant_reply and not interrupted:
        await speak_text_async(assistant_reply)

async def main_conversation():
    """Main conversation loop."""
    print("\n======================================")
    print("  Welcome to Happy Paws Dog Daycare!")
    print("  Voice Agent with Real-Time Supervisor")
    print("======================================\n")

    if DEMO_MODE:
        print("Running in DEMO MODE (text input)")
        print("Type 'exit' or 'quit' to stop\n")
    else:
        print("Running in VOICE MODE")
        print("Speak after the beep, silence will auto-stop recording")
        print("Say 'exit' or press Ctrl+C to stop\n")

    print("Rules being enforced:")
    print("  1. Only discuss dogs (no other pets)")
    print("  2. Get email before booking confirmation")
    print("  3. Required vaccines: Rabies and Distemper")
    print("  4. Hours: 7 AM-7 PM Mon-Sat, closed Sunday")
    print("  ...and more!\n")

    while True:
        try:
            user_text = await get_user_input()

            if not user_text:
                continue

            if user_text.lower() in ("exit", "quit"):
                print("\nThank you for visiting Happy Paws! Goodbye!")
                break

            await handle_turn(user_text)

        except KeyboardInterrupt:
            print("\nInterrupted by user")
            break
        except EOFError:
            # Handle EOF when running in non-interactive mode
            break
        except Exception as e:
            logger.error(f"Error in conversation loop: {e}")
            print("An error occurred. Please try again.")

async def main():
    """Main entry point."""
    try:
        # Test BAML connection
        print("Initializing...")

        # Run main conversation
        await main_conversation()

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        stop_tts()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        sys.exit(0)
