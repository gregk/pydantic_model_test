"""
Model utilities for the Maestro system.

This module provides utilities for working with AI model configurations
and selections, including validation and lookup functionality.
"""

from typing import Any, Dict, List, Literal, Optional, TypeAlias
from pydantic import BaseModel

# Define all known model names as a Literal type
KnownModelName: TypeAlias = str  # e.g., "anthropic:claude-3-sonnet-20240229"

# Model provider mapping
PROVIDER_PREFIXES = {
    "anthropic": ["claude"],
    "openai": ["gpt", "o1", "o3", "openai:gpt", "openai:o1", "openai:o3"],  # Include both prefixed and unprefixed
    "google-gla": ["gemini"],
    "google-vertex": ["gemini"],
    "cohere": ["command", "c4ai"],
    "groq": ["llama", "gemma", "mixtral", "deepseek", "qwen"],  # Updated Groq prefixes
    "mistral": ["mistral", "codestral"],
    "openrouter": ["o1", "o3"]  # OpenRouter supports various models
}

class ModelCapabilities(BaseModel):
    """Model capabilities configuration."""
    tools: bool = False
    function_calling: bool = False
    json_mode: bool = False
    system_prompt: bool = True
    vision: bool = False
    audio: bool = False

# Model registry
MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "anthropic:claude-3-5-sonnet-latest": {
        "provider": "anthropic",
        "base_name": "claude-3-5-sonnet",
        "capabilities": {
            "tools": True,
            "function_calling": True,
            "json_mode": True,
            "system_prompt": True,
            "vision": True,
            "audio": False
        }
    },
    "groq:deepseek-r1-distill-llama-70b-specdec": {
        "provider": "groq",
        "base_name": "deepseek-r1-distill-llama-70b",
        "capabilities": {
            "tools": False,
            "function_calling": False,
            "json_mode": True,
            "system_prompt": True,
            "vision": False,
            "audio": False
        }
    },
    "groq:qwen-2.5-coder-32b": {
        "provider": "groq",
        "base_name": "qwen-2.5-coder",
        "capabilities": {
            "tools": False,
            "function_calling": False,
            "json_mode": True,
            "system_prompt": True,
            "vision": False,
            "audio": False
        }
    }
}

def get_model_by_provider(provider: str, model_name: str) -> KnownModelName:
    """Get full model name from provider and base name.
    
    Args:
        provider: The provider name
        model_name: The base model name
        
    Returns:
        Full model identifier
    """
    return f"{provider}:{model_name}"

def get_latest_model(provider: str, base_name: str) -> KnownModelName:
    """Get latest version of a model.
    
    Args:
        provider: The provider name
        base_name: The base model name
        
    Returns:
        Full model identifier with latest version
    """
    return f"{provider}:{base_name}-latest"

def get_model_info(model: KnownModelName) -> Dict[str, Any]:
    """Get information about a model.
    
    Args:
        model: The model identifier
        
    Returns:
        Dict containing model information
        
    Raises:
        KeyError: If model is not found in registry
    """
    if model not in MODEL_REGISTRY:
        raise KeyError(f"Model {model} not found in registry")
    return MODEL_REGISTRY[model] 