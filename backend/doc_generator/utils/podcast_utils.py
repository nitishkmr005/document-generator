"""
Helpers for podcast workflow nodes.
"""

from __future__ import annotations

import json
import wave
from io import BytesIO
from typing import Any

from loguru import logger


def wave_bytes(
    pcm: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2
) -> bytes:
    """Convert PCM audio data to WAV format bytes."""
    with BytesIO() as wav_buffer:
        with wave.open(wav_buffer, "wb") as wav_file:
            wav_file.setnchannels(channels)
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(rate)
            wav_file.writeframes(pcm)
        return wav_buffer.getvalue()


def build_tts_prompt(dialogue: list[dict], speakers: list[dict]) -> str:
    """Build the TTS prompt from dialogue."""
    lines = []
    for entry in dialogue:
        speaker = entry.get("speaker", "Speaker")
        text = entry.get("text", "")
        if text.strip():
            lines.append(f"{speaker}: {text}")
    return "\n".join(lines)


def synthesize_with_retry(
    tts_prompt: str,
    speakers: list[dict],
    api_key: str,
    max_retries: int = 3,
) -> bytes:
    """Generate audio using Gemini TTS with retry logic."""
    import random
    import time

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    speaker_voice_configs = []
    for speaker in speakers:
        voice_name = speaker.get("voice", "Kore")
        speaker_voice_configs.append(
            types.SpeakerVoiceConfig(
                speaker=speaker["name"],
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=voice_name,
                    )
                ),
            )
        )

    last_error: Exception | None = None
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=tts_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                            speaker_voice_configs=speaker_voice_configs
                        )
                    ),
                ),
            )

            audio_data = response.candidates[0].content.parts[0].inline_data.data
            if attempt > 0:
                logger.info(f"TTS succeeded on attempt {attempt + 1}")
            return audio_data

        except Exception as e:
            last_error = e
            error_str = str(e).lower()

            retryable = any(
                p in error_str for p in ["500", "internal", "overload", "unavailable"]
            )

            if retryable and attempt < max_retries - 1:
                delay = (2**attempt) * (1 + random.uniform(0, 0.5))
                logger.warning(
                    "TTS error (attempt {}/{}): {}. Retrying in {:.1f}s...".format(
                        attempt + 1,
                        max_retries,
                        str(e)[:100],
                        delay,
                    )
                )
                time.sleep(delay)
            else:
                raise

    if last_error:
        raise last_error
    raise RuntimeError("TTS generation failed unexpectedly")


def extract_json(text: str) -> dict[str, Any] | None:
    """Extract JSON from text."""
    import re

    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    patterns = [
        r"```json\s*([\s\S]*?)\s*```",
        r"```\s*([\s\S]*?)\s*```",
        r"\{[\s\S]*\}",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                json_str = match.group(1) if "```" in pattern else match.group(0)
                return json.loads(json_str)
            except (json.JSONDecodeError, IndexError):
                continue

    return None
