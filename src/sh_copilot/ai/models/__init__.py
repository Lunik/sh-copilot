"""
This module contains the AI models used by the AI module.
"""

from typing import Dict, ClassVar

from pydantic import BaseModel

from sh_copilot.ai.models.base import BaseAIModel
from sh_copilot.ai.models.fake import FakeAIModel
from sh_copilot.ai.models.openai import OpenAIModel


class AIModelFactory(BaseModel):
    """
    Class used to retreive the appropriate AI model based on the name.
    """

    catalog: ClassVar[Dict[str, BaseAIModel]] = {
        FakeAIModel.name: FakeAIModel,
        OpenAIModel.name: OpenAIModel,
    }

    @classmethod
    def get_model(cls, name: str) -> BaseAIModel:
        """
        Return the appropriate AI model based on the name.
        """
        if name not in cls.catalog:
            raise ValueError(f"Invalid AI model name: {name}")

        return cls.catalog[name]
