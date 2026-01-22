"""Podcast audio synthesis node for unified workflow."""

from __future__ import annotations

import base64

from loguru import logger

from ..unified_state import UnifiedWorkflowState
from ...utils.podcast_utils import build_tts_prompt, synthesize_with_retry, wave_bytes


def synthesize_podcast_audio_node(
    state: UnifiedWorkflowState,
) -> UnifiedWorkflowState:
    """
    Synthesize audio from podcast script using Gemini TTS.

    Args:
        state: Current workflow state with podcast_dialogue

    Returns:
        Updated state with podcast_audio_base64
    """
    dialogue = state.get("podcast_dialogue", [])
    request_data = state.get("request_data", {})
    gemini_api_key = state.get("gemini_api_key") or state.get("api_key", "")

    if not dialogue:
        state["errors"] = state.get("errors", []) + [
            "No dialogue for audio synthesis"
        ]
        return state

    if not gemini_api_key:
        state["errors"] = state.get("errors", []) + [
            "Gemini API key required for TTS"
        ]
        return state

    speakers = request_data.get(
        "speakers",
        [
            {"name": "Alex", "voice": "Kore", "role": "host"},
            {"name": "Sam", "voice": "Puck", "role": "co-host"},
        ],
    )

    logger.info(f"Synthesizing audio for {len(dialogue)} dialogue entries")

    try:
        tts_prompt = build_tts_prompt(dialogue, speakers)
        audio_data = synthesize_with_retry(tts_prompt, speakers, gemini_api_key)

        wav_data = wave_bytes(audio_data)
        audio_base64 = base64.b64encode(wav_data).decode()

        state["podcast_audio_data"] = audio_data
        state["podcast_audio_base64"] = audio_base64
        state["podcast_duration_seconds"] = len(audio_data) / (
            24000 * 2
        )  # 24kHz, 16-bit
        state["completed"] = True

        logger.info(
            "Synthesized {:.1f}s of audio".format(
                state["podcast_duration_seconds"]
            )
        )

    except Exception as e:
        logger.error(f"Audio synthesis failed: {e}")
        state["errors"] = state.get("errors", []) + [
            f"Audio synthesis failed: {str(e)}"
        ]

    return state
