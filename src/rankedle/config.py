import yaml
import os
from typing import Any


class Config:

    def __init__(
        self,
        config_file=f"{os.path.dirname(os.path.realpath(__file__))}/config.yaml"
    ):
        self.config_file = config_file
        self.config = self._load()

    def _load(self) -> dict:
        """Load config file as dictionary."""
        try:
            with open(self.config_file, 'r') as file:
                config = yaml.safe_load(file)
                self._replace_env_vars(config)
                return config
        except FileNotFoundError:
            raise Exception(f"The file {self.config_file} was not found.")
        except yaml.YAMLError as e:
            raise Exception(f"Error reading YAML file: {e}")

    def _replace_env_vars(self, config: dict) -> None:
        """Replace environment variables for its value."""
        for section in config.values():
            if isinstance(section, dict):
                for key, value in section.items():
                    if isinstance(value, str) and value.startswith(
                            "${") and value.endswith("}"):
                        env_var = value[2:-1]  # Delete '${}'
                        env_value = os.getenv(env_var)
                        if env_value:
                            section[key] = env_value

    def get(self, section, key=None) -> Any:
        """Gets the value of a section and option in the configuration file."""
        section_data = self.config.get(section, {})
        if key:
            return section_data.get(key)
        return section_data
