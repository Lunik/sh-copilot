"""
Base AI model.
"""

from abc import ABC, abstractmethod
from typing import ClassVar

from pydantic import BaseModel, model_validator

from sh_copilot.ai.context import AIMessage, AIContext, ChunkedAIMessage


class BaseAIModel(BaseModel, ABC):
    """
    Base AI model.
    """

    name: ClassVar[str] = "base"
    """Name of the model."""

    __abstract__ = True

    @abstractmethod
    @model_validator(mode="after")
    def init_model(cls, values):  # pylint: disable=no-self-argument
        """
        Initialize the model.
        """

    @abstractmethod
    def chat_completion(self, context: AIContext) -> AIMessage:
        """
        Return a fake response.
        """

    @abstractmethod
    def chat_completion_stream(self, context: AIContext) -> ChunkedAIMessage:
        """
        Return a fake response.
        """
