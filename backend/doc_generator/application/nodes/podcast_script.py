"""Podcast script generation node for unified workflow."""

from __future__ import annotations

from loguru import logger

from ..unified_state import UnifiedWorkflowState
from ...utils.podcast_utils import extract_json


def generate_podcast_script_node(state: UnifiedWorkflowState) -> UnifiedWorkflowState:
    """
    Generate podcast script from extracted content.

    Uses LLM to create a dialogue-based script suitable for TTS synthesis.

    Args:
        state: Current workflow state with raw_content

    Returns:
        Updated state with podcast_script and podcast_dialogue
    """
    request_data = state.get("request_data", {})
    raw_content = state.get("summary_content") or state.get("raw_content", "")
    api_key = state.get("api_key", "")

    if not raw_content:
        state["errors"] = state.get("errors", []) + ["No content for podcast script"]
        return state

    style = request_data.get("style", "conversational")
    speakers = request_data.get(
        "speakers",
        [
            {"name": "Alex", "voice": "Kore", "role": "host"},
            {"name": "Sam", "voice": "Puck", "role": "co-host"},
        ],
    )
    duration_minutes = request_data.get("duration_minutes", 3)
    provider = request_data.get("provider", "gemini")
    model = request_data.get("model", "gemini-2.5-flash")

    logger.info(
        f"Generating podcast script: style={style}, duration={duration_minutes}min"
    )

    try:
        from ...infrastructure.llm import LLMService
        import os

        provider_name = provider if provider != "google" else "gemini"

        key_mapping = {
            "gemini": "GOOGLE_API_KEY",
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
        }
        env_var = key_mapping.get(provider_name)
        if env_var and api_key:
            os.environ[env_var] = api_key

        llm_service = LLMService(provider=provider_name, model=model)

        speaker_list = ", ".join([f"{s['name']} ({s['role']})" for s in speakers])
        source_count = state.get("metadata", {}).get("source_count", 1)

        prompt = f"""Generate a podcast script about the following content.

CONTENT:
{raw_content}

REQUIREMENTS:
- Style: {style}
- Target duration: {duration_minutes} minutes
- Speakers: {speaker_list}
- Based on {source_count} source document(s)

OUTPUT FORMAT (JSON):
{{
  \"title\": \"Episode title\",
  \"description\": \"Brief episode description\",
  \"dialogue\": [
    {{\"speaker\": \"SpeakerName\", \"text\": \"What they say...\"}},
    {{\"speaker\": \"OtherSpeaker\", \"text\": \"Their response...\"}}
  ]
}}

Create an engaging dialogue that covers the key points from the content.
The dialogue should feel natural and conversational."""

        response = llm_service.generate(prompt)

        script_json = extract_json(response)
        if not script_json:
            state["errors"] = state.get("errors", []) + [
                "Failed to parse podcast script"
            ]
            return state

        state["podcast_script"] = response
        state["podcast_dialogue"] = script_json.get("dialogue", [])
        state["podcast_title"] = script_json.get("title", "Podcast Episode")
        state["podcast_description"] = script_json.get("description", "")

        logger.info(
            "Generated script with {} dialogue entries".format(
                len(state["podcast_dialogue"])
            )
        )

    except Exception as e:
        logger.error(f"Podcast script generation failed: {e}")
        state["errors"] = state.get("errors", []) + [
            f"Script generation failed: {str(e)}"
        ]

    return state
