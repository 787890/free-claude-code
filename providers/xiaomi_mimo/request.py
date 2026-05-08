"""Request builder for Xiaomi MiMo native Anthropic Messages API.

MiMo only accepts a subset of Anthropic request fields. Unsupported fields
like ``metadata``, ``top_k``, ``mcp_servers``, ``context_management``, and
``output_config`` must be stripped before sending.
"""

from __future__ import annotations

from typing import Any

from loguru import logger

from config.constants import ANTHROPIC_DEFAULT_MAX_OUTPUT_TOKENS
from core.anthropic.native_messages_request import dump_raw_messages_request

_MIMO_SUPPORTED_FIELDS = frozenset(
    {
        "messages",
        "model",
        "max_tokens",
        "stop_sequences",
        "stream",
        "system",
        "temperature",
        "thinking",
        "tool_choice",
        "tools",
        "top_p",
    }
)


def build_request_body(request_data: Any, *, thinking_enabled: bool) -> dict:
    """Build an Anthropic-format request body with only MiMo-supported fields."""
    logger.debug(
        "XIAOMI_MIMO_REQUEST: build start model={} msgs={}",
        getattr(request_data, "model", "?"),
        len(getattr(request_data, "messages", [])),
    )

    data = dump_raw_messages_request(request_data)

    body: dict[str, Any] = {
        key: value
        for key, value in data.items()
        if key in _MIMO_SUPPORTED_FIELDS and value is not None
    }

    if "thinking" in body:
        thinking_cfg = body.pop("thinking")
        if thinking_enabled and isinstance(thinking_cfg, dict):
            thinking_payload: dict[str, Any] = {"type": "enabled"}
            budget_tokens = thinking_cfg.get("budget_tokens")
            if isinstance(budget_tokens, int):
                thinking_payload["budget_tokens"] = budget_tokens
            body["thinking"] = thinking_payload

    if "max_tokens" not in body or body.get("max_tokens") is None:
        body["max_tokens"] = ANTHROPIC_DEFAULT_MAX_OUTPUT_TOKENS

    body["stream"] = True

    logger.debug(
        "XIAOMI_MIMO_REQUEST: build done model={} msgs={} tools={}",
        body.get("model"),
        len(body.get("messages", [])),
        len(body.get("tools", [])),
    )
    return body
