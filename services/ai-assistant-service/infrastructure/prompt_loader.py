"""
Prompt loader — reads versioned YAML templates from the prompts/ directory.
Supports variable substitution via str.format_map().
"""
import os
import yaml
from typing import Dict, Optional
from pathlib import Path

_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
_cache: Dict[str, dict] = {}


def load_prompt(name: str, version: str = "v1") -> dict:
    """
    Load a prompt template by name and version.
    Returns dict with 'system' and 'user_template' keys.
    """
    key = f"{version}_{name}"
    if key in _cache:
        return _cache[key]

    path = _PROMPTS_DIR / f"{version}_{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Prompt template not found: {path}")

    with open(path) as f:
        data = yaml.safe_load(f)

    _cache[key] = data
    return data


def render_user_prompt(name: str, version: str = "v1", **kwargs) -> str:
    """Render the user_template with the provided variables."""
    template = load_prompt(name, version)
    return template["user_template"].format_map(kwargs)


def get_system_prompt(name: str, version: str = "v1") -> str:
    """Get the system prompt for a given template."""
    return load_prompt(name, version).get("system", "")
