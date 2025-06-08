import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class ConfigManager:
    """Configuration manager for LLM Knife library."""

    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._config:
            self._load_default_config()
            self._load_from_env()
            self._load_from_file()

    def _load_default_config(self):
        """Load default configuration values."""
        self._config = {
            "aws": {
                "region": "us-east-1",
                "bedrock": {
                    "anthropic": {
                        "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
                        "max_tokens": 1024,
                        "temperature": 0.7,
                    }
                },
            },
            "environment": os.getenv("LLM_KNIFE_ENV", "development"),
        }

    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_prefix = "LLM_KNIFE_"

        # AWS Configuration
        if aws_region := os.getenv(f"{env_prefix}AWS_REGION"):
            self._config["aws"]["region"] = aws_region

        # Anthropic Configuration
        if model_id := os.getenv(f"{env_prefix}ANTHROPIC_MODEL_ID"):
            self._config["aws"]["bedrock"]["anthropic"]["model_id"] = model_id

        if max_tokens := os.getenv(f"{env_prefix}MAX_TOKENS"):
            self._config["aws"]["bedrock"]["anthropic"]["max_tokens"] = int(max_tokens)

        if temperature := os.getenv(f"{env_prefix}TEMPERATURE"):
            self._config["aws"]["bedrock"]["anthropic"]["temperature"] = float(
                temperature
            )

    def _load_from_file(self):
        """Load configuration from config files."""
        config_paths = [
            Path.home() / ".llm_knife" / "config.yaml",
            Path.home() / ".llm_knife" / "config.json",
            Path.cwd() / "llm_knife_config.yaml",
            Path.cwd() / "llm_knife_config.json",
        ]

        for path in config_paths:
            if path.exists():
                try:
                    with open(path, "r") as f:
                        if path.suffix == ".yaml":
                            file_config = yaml.safe_load(f)
                        else:
                            file_config = json.load(f)

                        self._update_config(self._config, file_config)
                except Exception as e:
                    print(f"Warning: Could not load config from {path}: {str(e)}")

    def _update_config(self, base: Dict, update: Dict):
        """Recursively update configuration dictionary."""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._update_config(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        :param key: Configuration key (e.g., 'aws.bedrock.anthropic.model_id')
        :param default: Default value if key is not found
        :return: Configuration value
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """
        Set configuration value using dot notation.

        :param key: Configuration key (e.g., 'aws.bedrock.anthropic.model_id')
        :param value: Value to set
        """
        keys = key.split(".")
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def save_to_file(self, path: Optional[Path] = None):
        """
        Save current configuration to a file.

        :param path: Path to save configuration to (default: ~/.llm_knife/config.yaml)
        """
        if path is None:
            path = Path.home() / ".llm_knife" / "config.yaml"

        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            if path.suffix == ".yaml":
                yaml.dump(self._config, f, default_flow_style=False)
            else:
                json.dump(self._config, f, indent=2)


# Create a singleton instance
config = ConfigManager()
