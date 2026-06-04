"""
Qwen Cloud LLM Integration.

A thin wrapper around Qwen Cloud's OpenAI-compatible API.
Supports Qwen3.7-Max, Qwen3.6-Plus, Qwen3-Coder, and other models.

Intentionally does NOT use LangChain — keeping the dependency surface
minimal and the abstractions under our control.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

from openai import AsyncOpenAI


# ──────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────


@dataclass
class QwenConfig:
    """Configuration for Qwen Cloud API access."""

    api_key: str = field(default_factory=lambda: os.getenv("QWEN_API_KEY", ""))
    base_url: str = field(
        default_factory=lambda: os.getenv(
            "QWEN_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
        )
    )
    default_model: str = "qwen3.7-max"  # Best for reasoning/negotiation

    # Model selection by task
    reasoning_model: str = "qwen3.7-max"
    coding_model: str = "qwen3-coder-480b-a35b"
    general_model: str = "qwen3.6-plus"

    # Generation defaults
    max_tokens: int = 4096
    temperature: float = 0.7
    top_p: float = 0.9

    # Rate limiting
    max_retries: int = 3
    retry_delay: float = 1.0


# ──────────────────────────────────────────────────────────────
# Qwen Client Wrapper
# ──────────────────────────────────────────────────────────────


class QwenClient:
    """
    Async client for Qwen Cloud models.

    Usage:
        client = QwenClient(QwenConfig(api_key="..."))
        response = await client.chat([
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ])
    """

    def __init__(self, config: QwenConfig | None = None) -> None:
        self.config = config or QwenConfig()

        if not self.config.api_key:
            raise ValueError(
                "Qwen API key not found. Set QWEN_API_KEY environment variable "
                "or pass it in QwenConfig. Get your key at: "
                "https://modelstudio.alibabacloud.com"
            )

        self._client = AsyncOpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            max_retries=self.config.max_retries,
        )

    async def chat(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        response_format: dict[str, str] | None = None,
    ) -> str:
        """
        Send a chat completion request and return the response text.
        """
        model = model or self.config.default_model
        temperature = temperature if temperature is not None else self.config.temperature
        max_tokens = max_tokens or self.config.max_tokens

        kwargs: dict[str, Any] = {
            "model": model,
            "messages": messages,  # type: ignore[arg-type]
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": self.config.top_p,
        }

        if response_format is not None:
            kwargs["response_format"] = response_format

        response = await self._client.chat.completions.create(**kwargs)

        content = response.choices[0].message.content
        return content or ""

    async def chat_structured(
        self,
        messages: list[dict[str, str]],
        output_schema: dict[str, Any],
        model: str | None = None,
        temperature: float | None = None,
    ) -> dict[str, Any]:
        """
        Send a chat completion and parse the response as structured JSON.

        Uses the model's native JSON mode for reliable structured output.
        """
        # Add schema instruction to system message
        schema_instruction = (
            f"\n\nYou MUST respond with valid JSON matching this schema:\n"
            f"{json.dumps(output_schema, indent=2)}\n"
            f"Do not include any text outside the JSON object."
        )

        augmented_messages = list(messages)
        if augmented_messages and augmented_messages[0]["role"] == "system":
            augmented_messages[0]["content"] += schema_instruction
        else:
            augmented_messages.insert(0, {
                "role": "system",
                "content": f"Respond with JSON:{schema_instruction}",
            })

        raw = await self.chat(
            messages=augmented_messages,
            model=model,
            temperature=temperature or 0.3,  # Lower temp for structured output
            response_format={"type": "json_object"},
        )

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Attempt to extract JSON from the response
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(raw[start:end])
            raise ValueError(f"Failed to parse structured response as JSON: {raw[:200]}...")

    async def agent_reason(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
        temperature: float | None = None,
    ) -> str:
        """
        Convenience method for agent reasoning tasks (system + user prompt).
        """
        return await self.chat(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model=model or self.config.reasoning_model,
            temperature=temperature,
        )

    async def agent_code(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Convenience method for code-related agent tasks.
        Uses Qwen3-Coder model.
        """
        return await self.chat(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model=self.config.coding_model,
            temperature=0.3,  # Lower temp for code generation
        )

    # ── Connection test ───────────────────────────────────

    async def ping(self) -> bool:
        """Test connectivity to Qwen Cloud."""
        try:
            await self.chat(
                messages=[{"role": "user", "content": "Reply with just 'pong'."}],
                max_tokens=10,
            )
            return True
        except Exception:
            return False
