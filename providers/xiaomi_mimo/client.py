"""Xiaomi MiMo provider implementation (native Anthropic-compatible Messages)."""

from __future__ import annotations

from typing import Any

from providers.anthropic_messages import AnthropicMessagesTransport
from providers.base import ProviderConfig
from providers.defaults import XIAOMI_MIMO_DEFAULT_BASE
from providers.model_listing import ProviderModelInfo

from .request import build_request_body

_HARDCODED_MODEL_ID = "mimo-v2.5-pro"


class XiaomiMiMoProvider(AnthropicMessagesTransport):
    """Xiaomi MiMo using ``https://token-plan-cn.xiaomimimo.com/anthropic/v1/messages`` (Anthropic Messages API)."""

    def __init__(self, config: ProviderConfig):
        super().__init__(
            config,
            provider_name="XIAOMI_MIMO",
            default_base_url=XIAOMI_MIMO_DEFAULT_BASE,
        )

    def _build_request_body(
        self, request: Any, thinking_enabled: bool | None = None
    ) -> dict:
        return build_request_body(
            request,
            thinking_enabled=self._is_thinking_enabled(request, thinking_enabled),
        )

    def _request_headers(self) -> dict[str, str]:
        return {
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
            "api-key": self._api_key,
        }

    async def list_model_infos(self) -> frozenset[ProviderModelInfo]:
        """Return the hardcoded MiMo model id until a discovery endpoint is available."""
        return frozenset(
            {ProviderModelInfo(model_id=_HARDCODED_MODEL_ID, supports_thinking=None)}
        )
