"""
Checkpoint management for unified workflow.

Provides session-based state persistence using LangGraph's checkpointing feature.
This enables:
- Reusing enhanced content across different output formats
- Resuming workflows from failure points
- Caching intermediate processing steps
"""

import hashlib
import json
import os
import time
from pathlib import Path
from threading import Lock
from typing import Any, Optional

from loguru import logger

# Try to import LangGraph checkpointers
try:
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.checkpoint.sqlite import SqliteSaver

    HAS_SQLITE_SAVER = True
except ImportError:
    from langgraph.checkpoint.memory import MemorySaver

    HAS_SQLITE_SAVER = False
    logger.warning("SqliteSaver not available, using MemorySaver only")


class CheckpointManager:
    """
    Manages workflow checkpoints for session-based state persistence.

    Features:
    - Content-based session IDs for automatic deduplication
    - In-memory and SQLite persistence options
    - Automatic checkpoint expiration
    - Thread-safe operations
    """

    _instance: Optional["CheckpointManager"] = None
    _lock = Lock()

    def __new__(cls) -> "CheckpointManager":
        """Singleton pattern for checkpoint manager."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize checkpoint manager."""
        if self._initialized:
            return

        self._initialized = True
        self._memory_saver = MemorySaver()
        self._sqlite_saver = None
        self._session_metadata: dict[str, dict] = {}
        self._checkpoint_dir = Path(
            os.getenv("CHECKPOINT_DIR", "/tmp/prismdocs_checkpoints")
        )

        # Initialize SQLite saver if available and enabled
        if (
            HAS_SQLITE_SAVER
            and os.getenv("USE_SQLITE_CHECKPOINTS", "false").lower() == "true"
        ):
            self._init_sqlite_saver()

        logger.info(
            f"CheckpointManager initialized, using {'SQLite' if self._sqlite_saver else 'Memory'} storage"
        )

    def _init_sqlite_saver(self):
        """Initialize SQLite-based checkpointer for persistence."""
        try:
            self._checkpoint_dir.mkdir(parents=True, exist_ok=True)
            db_path = self._checkpoint_dir / "checkpoints.db"
            self._sqlite_saver = SqliteSaver.from_conn_string(str(db_path))
            logger.info(f"SQLite checkpointer initialized at {db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize SQLite checkpointer: {e}")
            self._sqlite_saver = None

    @property
    def checkpointer(self):
        """Get the active checkpointer (SQLite if available, else Memory)."""
        return self._sqlite_saver or self._memory_saver

    def generate_session_id(
        self,
        sources: list[dict],
        user_id: Optional[str] = None,
    ) -> str:
        """
        Generate a content-based session ID.

        Same sources + user = same session ID, enabling checkpoint reuse.

        Args:
            sources: List of source items (files, URLs, text)
            user_id: Optional user identifier

        Returns:
            Deterministic session ID based on content hash
        """
        # Normalize sources for consistent hashing
        normalized = []
        for src in sorted(sources, key=lambda x: json.dumps(x, sort_keys=True)):
            src_type = src.get("type", "")
            if src_type == "file":
                normalized.append(f"file:{src.get('file_id', '')}")
            elif src_type == "url":
                normalized.append(f"url:{src.get('url', '')}")
            elif src_type == "text":
                # Hash text content to avoid huge IDs
                text_hash = hashlib.md5(src.get("content", "").encode()).hexdigest()[
                    :16
                ]
                normalized.append(f"text:{text_hash}")

        # Create session ID from sources + user
        content_str = "|".join(normalized)
        if user_id:
            content_str += f"|user:{user_id}"

        session_hash = hashlib.sha256(content_str.encode()).hexdigest()[:24]
        return f"session_{session_hash}"

    def get_checkpoint_config(
        self,
        session_id: str,
        checkpoint_ns: str = "",
    ) -> dict:
        """
        Get configuration dict for LangGraph checkpoint operations.

        Args:
            session_id: Session identifier
            checkpoint_ns: Optional namespace for checkpoints

        Returns:
            Config dict compatible with LangGraph invoke/stream
        """
        config = {
            "configurable": {
                "thread_id": session_id,
            }
        }
        if checkpoint_ns:
            config["configurable"]["checkpoint_ns"] = checkpoint_ns
        return config

    def has_checkpoint(
        self, session_id: str, node_name: str = "extract_sources"
    ) -> bool:
        """
        Check if a checkpoint exists for the given session.

        Args:
            session_id: Session identifier
            node_name: Name of the node to check checkpoint for

        Returns:
            True if checkpoint exists
        """
        try:
            config = self.get_checkpoint_config(session_id)
            checkpoint = self.checkpointer.get(config)
            if checkpoint:
                # Check if we have processed past the specified node
                ts = checkpoint.get("ts", "")
                logger.debug(f"Found checkpoint for session {session_id}: ts={ts}")
                return True
            return False
        except Exception as e:
            logger.debug(f"Error checking checkpoint: {e}")
            return False

    def get_session_metadata(self, session_id: str) -> dict:
        """
        Get metadata for a session.

        Args:
            session_id: Session identifier

        Returns:
            Session metadata dict
        """
        return self._session_metadata.get(session_id, {})

    def set_session_metadata(
        self,
        session_id: str,
        key: str,
        value: Any,
    ):
        """
        Set metadata for a session.

        Args:
            session_id: Session identifier
            key: Metadata key
            value: Metadata value
        """
        if session_id not in self._session_metadata:
            self._session_metadata[session_id] = {
                "created_at": time.time(),
                "outputs_generated": [],
            }
        self._session_metadata[session_id][key] = value

    def record_output_generated(
        self,
        session_id: str,
        output_type: str,
    ):
        """
        Record that an output type was generated for this session.

        Args:
            session_id: Session identifier
            output_type: Type of output generated
        """
        if session_id not in self._session_metadata:
            self._session_metadata[session_id] = {
                "created_at": time.time(),
                "outputs_generated": [],
            }

        outputs = self._session_metadata[session_id].get("outputs_generated", [])
        if output_type not in outputs:
            outputs.append(output_type)
        self._session_metadata[session_id]["outputs_generated"] = outputs
        self._session_metadata[session_id]["last_generated"] = output_type
        self._session_metadata[session_id]["last_generated_at"] = time.time()

    def cleanup_expired_sessions(self, max_age_seconds: int = 3600):
        """
        Remove sessions older than max_age_seconds.

        Args:
            max_age_seconds: Maximum session age in seconds (default: 1 hour)
        """
        current_time = time.time()
        expired = []

        for session_id, metadata in self._session_metadata.items():
            created_at = metadata.get("created_at", 0)
            if current_time - created_at > max_age_seconds:
                expired.append(session_id)

        for session_id in expired:
            del self._session_metadata[session_id]
            logger.debug(f"Cleaned up expired session: {session_id}")

        if expired:
            logger.info(f"Cleaned up {len(expired)} expired sessions")


# Global checkpoint manager instance
_checkpoint_manager: Optional[CheckpointManager] = None


def get_checkpoint_manager() -> CheckpointManager:
    """Get or create the global checkpoint manager."""
    global _checkpoint_manager
    if _checkpoint_manager is None:
        _checkpoint_manager = CheckpointManager()
    return _checkpoint_manager
