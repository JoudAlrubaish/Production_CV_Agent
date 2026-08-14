from __future__ import annotations

import os
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np
import sounddevice as sd
from dotenv import load_dotenv

from agent.agent import build_client, run_agent

load_dotenv()

SAMPLE_RATE = int(os.getenv("VOICE_SAMPLE_RATE", "16000"))
RECORD_SECONDS = float(os.getenv("VOICE_RECORD_SECONDS", "6"))
STT_MODEL = os.getenv("STT_MODEL", "whisper-1")
VOICE_LANGUAGE = os.getenv("VOICE_LANGUAGE", "en")


def record_wav(path: Path, seconds: float = RECORD_SECONDS) -> None:
    """Record microphone audio and save it as a mono 16-bit WAV file."""
    print(f"\n🎙️  Recording for {seconds:g} seconds... Speak now.")
    audio = sd.rec(
        int(seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()

    pcm16 = np.clip(audio[:, 0], -1.0, 1.0)
    pcm16 = (pcm16 * 32767).astype(np.int16)

    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(pcm16.tobytes())


def transcribe_audio(path: Path) -> str:
    """Convert recorded speech to text using the configured OpenAI STT model."""
    client = build_client()
    with path.open("rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model=STT_MODEL,
            file=audio_file,
            language=VOICE_LANGUAGE or None,
        )
    return transcript.text.strip()


def speak(text: str) -> None:
    """Speak the agent answer on macOS using the built-in `say` command."""
    if not text:
        return
    try:
        subprocess.run(["say", text], check=False)
    except FileNotFoundError:
        # Non-macOS environments can still use voice input + text output.
        pass


def voice_turn(seconds: float = RECORD_SECONDS) -> None:
    """Voice Input -> STT -> Agent -> Tool Calls -> Spoken/Text Response."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        wav_path = Path(temp_file.name)

    try:
        record_wav(wav_path, seconds)
        user_text = transcribe_audio(wav_path)

        if not user_text:
            print("I could not detect speech. Please try again.")
            return

        print(f"You (voice): {user_text}")
        answer = run_agent(user_text)
        print(f"Agent: {answer}")
        speak(answer)
    finally:
        wav_path.unlink(missing_ok=True)


def main() -> None:
    print("Production CV Voice Agent")
    print("Press Enter to record a question, or type 'exit' to stop.")
    print(f"Recording length: {RECORD_SECONDS:g} seconds")

    while True:
        command = input("\nPress Enter to speak: ").strip().lower()
        if command in {"exit", "quit"}:
            break

        try:
            voice_turn()
        except KeyboardInterrupt:
            print("\nVoice recording cancelled.")
        except Exception as exc:
            print(f"Voice agent error: {exc}")


if __name__ == "__main__":
    main()