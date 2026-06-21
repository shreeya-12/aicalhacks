"""Shared helper for building Anthropic tool input_schemas from Pydantic models.

Forcing tool-use (via tool_choice) instead of asking Claude to write prose JSON
makes malformed output structurally impossible — there's no free-text wrapper
(markdown fences, "Here's the result:" preambles) left for Claude to add.
"""

from pydantic import BaseModel


def input_schema_for(model: type[BaseModel], wrapper_key: str, count: int) -> dict:
    """Builds a tool input_schema of shape {wrapper_key: [<count> x model]}.

    count is enforced via minItems/maxItems on the wrapper array — this can't
    be derived from the item model alone, so it's added explicitly here.
    """
    item_schema = model.model_json_schema()
    item_schema.pop("title", None)
    return {
        "type": "object",
        "properties": {
            wrapper_key: {
                "type": "array",
                "items": item_schema,
                "minItems": count,
                "maxItems": count,
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
