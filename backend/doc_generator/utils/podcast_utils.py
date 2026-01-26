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
    """Extract JSON object from text."""
    if not text:
        return None

    def _parse_candidate(candidate: str) -> dict[str, Any] | None:
        try:
            parsed = json.loads(candidate)
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            return None

    direct = _parse_candidate(text)
    if direct is not None:
        return direct

    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    cleaned_parsed = _parse_candidate(cleaned)
    if cleaned_parsed is not None:
        return cleaned_parsed

    start_idx = cleaned.find("{")
    if start_idx == -1:
        return None

    brace_count = 0
    in_string = False
    escape_next = False

    for i in range(start_idx, len(cleaned)):
        ch = cleaned[i]
        if escape_next:
            escape_next = False
            continue
        if ch == "\\":
            escape_next = True
            continue
        if ch == '"' and not escape_next:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            brace_count += 1
        elif ch == "}":
            brace_count -= 1
            if brace_count == 0:
                return _parse_candidate(cleaned[start_idx : i + 1])

    return None
