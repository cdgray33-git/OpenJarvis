from typing import Tuple, Dict

class ModelSpec:
    def __init__(
        self,
        model_id: str,
        name: str,
        parameter_count_b: float,
        context_length: int,
        supported_engines: Tuple[str, ...],
        provider: str,
        requires_api_key: bool,
        metadata: Dict[str, any]
    ):
        self.model_id = model_id
        self.name = name
        self.parameter_count_b = parameter_count_b
        self.context_length = context_length
        self.supported_engines = supported_engines
        self.provider = provider
        self.requires_api_key = requires_api_key
        self.metadata = metadata

BUILTIN_MODELS = [
    ModelSpec(
        model_id="qwen/qwen3-coder:free",
        name="Qwen3-Coder-480B-A35B-Instruct",
        parameter_count_b=480.0,
        context_length=1_000_000,  # 1M tokens
        supported_engines=("openrouter",),
        provider="Alibaba Cloud",
        requires_api_key=True,  # Assuming an API key is required for OpenRouter
        metadata={
            "pricing": "Free",
            "url": "https://www.openrouter.com/models/qwen3-coder-480b-a35b-instruct",
            "weekly_tokens": 32_000_000_000,  # 32B tokens
            "released": "2025-07-22"
        }
    ),
    ModelSpec(
        model_id="google/gemma-4-31b-it:free",
        name="Gemma 4 31B Instruct",
        parameter_count_b=31.0,
        context_length=262_144,  # 256K tokens
        supported_engines=("openrouter", "google"),
        provider="Google DeepMind",
        requires_api_key=True,  # Assuming an API key is required for OpenRouter
        metadata={
            "pricing": "Free",
            "url": "https://www.openrouter.com/models/gemma-4-31b-it",
            "license": "Apache 2.0"
        }
    ),
]

def register_builtin_models(model_registry):
    for model in BUILTIN_MODELS:
        if model.model_id not in model_registry:
            model_registry[model.model_id] = model

def merge_discovered_models(engine_key, model_ids, model_registry):
    for model_id in model_ids:
        if model_id not in model_registry:
            # Create a minimal ModelSpec entry
            model_registry[model_id] = ModelSpec(
                model_id=model_id,
                name=model_id,
                parameter_count_b=0.0,
                context_length=0,
                supported_engines=(engine_key,),
                provider="Unknown",
                requires_api_key=True,
                metadata={}
            )

# Example usage
if __name__ == "__main__":
    model_registry = {}

    register_builtin_models(model_registry)

    # If you have discovered models from OpenRouter, you can merge them like this:
    discovered_openrouter_models = [
        "qwen/qwen3-coder:free",  # Ensure this is included if not already in BUILTIN_MODELS
        "google/gemma-4-31b-it:free"
    ]

    merge_discovered_models("openrouter", discovered_openrouter_models, model_registry)

    # If you have discovered models from Google, you can merge them like this:
    discovered_google_models = [
        "google/gemma-4-31b-it:free"  # Ensure this is included if not already in BUILTIN_MODELS
    ]

    merge_discovered_models("google", discovered_google_models, model_registry)

    # Print the registered models to verify
    for model_id, model_spec in model_registry.items():
        print(f"Model ID: {model_id}, Name: {model_spec.name}, Provider: {model_spec.provider}, Pricing: {model_spec.metadata.get('pricing', 'Unknown')}")