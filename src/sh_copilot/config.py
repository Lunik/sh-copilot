"""
Shell Copilot Configuration
"""

import os
import subprocess
from typing import Self, Dict, Any

import yaml

from pydantic import BaseModel


class Config(BaseModel):
    """
    Shell Copilot configuration.
    """

    config_path: str = os.path.expanduser("~/.config/sh_copilot.yaml")
    """Path to the configuration file."""

    model: Dict[str, Any] = {}
    """Model configuration."""

    context: Dict[str, Any] = {}
    """Context configuration."""

    copilot: Dict[str, Any] = {}
    """Copilot configuration."""

    def init(self) -> None:
        """
        Initialize the configuration.
        """
        if not os.path.exists(self.config_path):
            with open(self.config_path, "w", encoding="utf-8") as file:
                file.write("---\n")

    def load(self) -> Self:
        """
        Load the configuration.
        """
        self.init()

        with open(self.config_path, "r", encoding="utf-8") as file:
            content = yaml.safe_load(file)

        if content is None:
            content = {}

        for key, value in content.items():
            if hasattr(self, key):
                setattr(self, key, value)

        return self

    def edit(self) -> Self:
        """
        Edit the configuration.
        """
        self.init()
        editor = os.environ.get("EDITOR", "vim")

        subprocess.call([editor, self.config_path])

        return self.load()
