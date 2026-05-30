"""Multi-engine wrapper — routes requests to the right backend by model name."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator, Sequence
from typing import Any, Dict, List

from openjarvis.core.types import Message
from openjarvis.engine._base import InferenceEngine
from openjarvis.engine._stubs import StreamChunk

logger = logging.getLogger(__name__)


class MultiEngine(InferenceEngine):
    """Wraps multiple engines and routes by model name.

    Models from each engine are discovered via ``list_models()``.
    When ``generate()`` or ``stream()`` is called, the model name
    is looked up to find which engine owns it.
    """

    engine_id = "multi"

    def __init__(self, engines: list[tuple[str, InferenceEngine]]) -> None:
        self._engines = engines
        self._model_map: Dict[str, InferenceEngine] = {}
        self._refresh_map()

    def _refresh_map(self) -> None:
        self._model_map.clear()
        for _key, engine in self._engines:
            try:
                for model_id in engine.list_models():
                    self._model_map[model_id] = engine
            except Exception as exc:
                logger.debug("Failed to list models for %s: %s", _key, exc)

    _CLOUD_PREFIXES = ("gpt-", "o1-", "o3-", "o4-", "claude-", "gemini-", "openrouter/")

    def _engine_for(self, model: str) -> InferenceEngine:
        """Find the engine that owns a model, refreshing the map once if needed."""
        engine = self._model_map.get(model)
        if engine is not None:
            return engine
        
        # Refresh and retry (a new model may have been pulled)
        self._refresh_map()
        engine = self._model_map.get(model)
        if engine is not None:
            return engine
        
        # FIXED: Better error handling for cloud vs local models
        if any(model.startswith(p) for p in self._CLOUD_PREFIXES):
            for key, eng in self._engines:
                if key == "cloud":
                    logger.info("Routing cloud model %r to cloud engine", model)
                    return eng
            # Cloud model requested but no cloud engine available
            raise ValueError(
                f"Cloud model {model!r} requested but no cloud engine configured. "
                f"Add API keys in ~/.openjarvis/cloud-keys.env or via the Cloud Models tab in the UI."
            )
        
        # Local model requested - provide helpful error
        available = ', '.join(sorted(self._model_map.keys())) if self._model_map else 'none'
        
        # FIXED: Handle empty engine list explicitly
        if not self._engines:
            raise ValueError(
                f"No inference engines configured. "
                f"Install and start an engine (vLLM, llama.cpp, etc.) or use cloud models (gpt-*, claude-*, gemini-*)."
            )
        
        raise ValueError(
            f"Local model {model!r} not found in any configured engine. "
            f"Available models: {available}. "
            f"To use this model: pull it with your local engine or use a cloud model."
        )

    def generate(
        self,
        messages: Sequence[Message],
        *,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        return self._engine_for(model).generate(
            messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

    async def stream(
        self,
        messages: Sequence[Message],
        *,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        async for token in self._engine_for(model).stream(
            messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        ):
            yield token

    async def stream_full(
        self,
        messages: Sequence[Message],
        *,
        model: str,
        **kwargs: Any,
    ) -> AsyncIterator["StreamChunk"]:
        """Delegate stream_full() to the engine that owns the model."""
        engine = self._engine_for(model)
        async for chunk in engine.stream_full(messages, model=model, **kwargs):
            yield chunk

    def list_models(self) -> List[str]:
        self._refresh_map()
        return list(self._model_map.keys())

    def health(self) -> bool:
        return any(engine.health() for _key, engine in self._engines)

    def close(self) -> None:
        for _key, engine in self._engines:
            engine.close()


__all__ = ["MultiEngine"]
