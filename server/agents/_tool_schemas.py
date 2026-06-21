"""Shared helper for building Anthropic tool input_schemas from Pydantic models.

Forcing tool-use (via tool_choice) instead of asking Claude to write prose JSON
makes malformed output structurally impossible — there's no free-text wrapper
(markdown fences, "Here's the result:" preambles) left for Claude to add.
"""

from __future__ import annotations

from pydantic import BaseModel


def input_schema_for(model: type[BaseModel], wrapper_key: str, min_count: int, max_count: int | None = None) -> dict:
    """Builds a tool input_schema of shape {wrapper_key: [model, ...]}.

    Item count is enforced via minItems/maxItems on the wrapper array — this
    can't be derived from the item model alone, so it's added explicitly
    here. Pass only min_count for an exact count, or both for a range.
    """
    if max_count is None:
        max_count = min_count
    item_schema = model.model_json_schema()
    item_schema.pop("title", None)
    return {
        "type": "object",
        "properties": {
            wrapper_key: {
                "type": "array",
                "items": item_schema,
                "minItems": min_count,
                "maxItems": max_count,
            }
        },
        "required": [wrapper_key],
    }


def single_input_schema_for(model: type[BaseModel]) -> dict:
    """Builds a tool input_schema for submitting exactly one instance of model
    directly (no array wrapper) — used when a call produces a single object."""
    schema = model.model_json_schema()
    schema.pop("title", None)
    return schema
