"""
Fake AI model for testing purposes.
"""

from typing import ClassVar
from pydantic import model_validator

from sh_copilot.ai.models.base import BaseAIModel
from sh_copilot.ai.context import AIMessage, AIContext, AIAuthorType


class FakeAIModel(BaseAIModel):
    """
    Fake AI model for testing purposes.
    """

    name: ClassVar[str] = "fake"
    """Name of the model."""

    @model_validator(mode="after")
    def init_model(cls, values):  # pylint: disable=no-self-argument
        """
        Initialize the model.
        """

        return values

    def chat_completion(self, context: AIContext) -> AIMessage:
        """
        Return a fake response.
        """
        return AIMessage(content="This is a fake response.", author=AIAuthorType.AI)
