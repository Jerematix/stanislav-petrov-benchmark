"""Configuration management for Stanislav Petrov Benchmark."""

from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import logfire as lf
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    openrouter_api_key: str = Field(..., env="OPENROUTER_API_KEY")
    logfire_project_key: str = Field("", env="LOGFIRE_PROJECT_KEY")

    # Models to benchmark (OpenRouter model IDs)
    models: List[str] = Field(
        default=[
            "google/gemini-3-flash-preview",
            "anthropic/claude-haiku-4.5",
            "openai/gpt-5.2",
            "z-ai/glm-4.7",
            "moonshotai/kimi-k2-thinking",
        ]
    )

    # Scenario types
    scenarios: List[str] = Field(
        default=["nationalistic", "humanitarian", "destructive"]
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


def setup_logfire(project_key: str) -> None:
    """Initialize Logfire for observability with Pydantic AI instrumentation.

    Args:
        project_key: Logfire project key (empty to disable)
    """
    if project_key:
        lf.configure(
            token=project_key,
            service_name="stanislav-petrov-benchmark",
        )
        # Enable automatic Pydantic AI instrumentation
        # This captures all agent runs, tool calls, and responses automatically
        lf.instrument_pydantic_ai()
        lf.info("Logfire initialized with Pydantic AI instrumentation")
    else:
        # Log to console only if no project key provided
        lf.configure(
            send_to_logfire=False,
        )
        lf.info("Logfire running in console-only mode")


# Global settings instance
settings = Settings()

# Initialize Logfire
setup_logfire(settings.logfire_project_key)
