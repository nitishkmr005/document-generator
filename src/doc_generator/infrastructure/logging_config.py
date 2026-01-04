"""
Logging configuration for document generator.

Configures loguru for structured logging with custom formatting.
"""

import sys
from loguru import logger


def setup_logging(verbose: bool = False, log_file: str | None = None) -> None:
    """
    Configure logging for the application.

    Args:
        verbose: Enable debug logging if True
        log_file: Path to log file (optional)
    """
    # Remove default logger
    logger.remove()

    # Determine log level
    level = "DEBUG" if verbose else "INFO"

    # Console logging with color
    logger.add(
        sys.stderr,
        level=level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    # File logging if requested
    if log_file:
        logger.add(
            log_file,
            level=level,
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | "
                "{level: <8} | "
                "{name}:{function}:{line} - "
                "{message}"
            ),
            rotation="10 MB",
            retention="7 days",
        )
        logger.info(f"Logging to file: {log_file}")

    logger.info(f"Logging configured (level={level})")
