# Configuration Patterns

## File Locations

```
project/
├── config/
│   └── settings.yaml    # Main configuration (outside src/)
├── .env                  # Secrets and environment vars (root)
└── src/
    └── project/
        └── infrastructure/
            └── settings.py  # Pydantic Settings loader
```

> [!IMPORTANT]
>
> - Configuration YAML files go in `config/` (outside `src/`)
> - Secrets go in `.env` at project root
> - Never commit `.env` to git

## settings.yaml Structure

```yaml
# config/settings.yaml

# Application settings
app:
  name: "project-name"
  version: "0.1.0"
  debug: false

# Logging
logging:
  level: "INFO"
  format: "..."

# Feature-specific settings
feature:
  option1: "value"
  option2: 123
```

## Pydantic Settings

```python
# src/project/infrastructure/settings.py

from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    name: str = "project-name"
    version: str = "0.1.0"
    debug: bool = False


class LoggingSettings(BaseModel):
    level: str = "INFO"
    format: str = "..."


class Settings(BaseSettings):
    """Main settings loaded from YAML and .env"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PROJECT_",  # e.g., PROJECT_DEBUG=true
        extra="ignore",
    )

    # API Keys (from .env)
    anthropic_api_key: str | None = None
    openai_api_key: str | None = None
    google_api_key: str | None = None

    # Nested settings (from YAML)
    app: AppSettings = AppSettings()
    logging: LoggingSettings = LoggingSettings()


def load_yaml_config() -> dict:
    """Load config from YAML file."""
    config_path = Path("config/settings.yaml")
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {}


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    yaml_config = load_yaml_config()
    return Settings(**yaml_config)


# Convenience export
settings = get_settings()
```

## .env File

```bash
# .env (never commit this file!)

# API Keys
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# Optional overrides
PROJECT_DEBUG=true
```

## Environment Variable Override

Pydantic Settings supports env var overrides with prefix:

```bash
# Override app.debug via env var
PROJECT_DEBUG=true python -m project_name
```

## Usage in Code

```python
from project.config import settings

# Access API keys
api_key = settings.anthropic_api_key

# Access nested settings
log_level = settings.logging.level
```
