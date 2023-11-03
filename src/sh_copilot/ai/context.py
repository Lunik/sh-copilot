"""
Define the context for the AI.
"""

from typing import List, Optional
from enum import Enum

from pydantic import BaseModel


class AIAuthorType(Enum):
    """
    Enum for the AI author type.
    """

    HUMAN = "human"
    """Human."""

    AI = "ai"
    """AI."""


class AIMessage(BaseModel):
    """
    AI message.
    """

    author: AIAuthorType
    """Who sent the message."""

    content: str
    """The message."""

    def __str__(self) -> str:
        """
        Return the message.
        """
        return f"{self.author.value} > {self.content}"


class ChunkedAIMessage(BaseModel):
    """
    AI message.
    """

    author: Optional[AIAuthorType] = None
    """Who sent the message."""

    content: Optional[str] = None
    """The message."""

    def __str__(self) -> str:
        """
        Return the message.
        """
        if self.author is None:
            return self.content

        if self.content is None:
            return f"{self.author.value} > "

        return f"{self.author.value} > {self.content}"


class AIContext(BaseModel):
    """
    Base class for the AI context.
    """

    max_history: int = 10
    """The maximum history length."""

    conversation: List[AIMessage] = [
        AIMessage(
            author=AIAuthorType.AI,
            content="""
            You are an helpful assistant for the Shell.
            A user will ask you questions about command line he is typing.
            You will help him troubleshoot his problems.
            You will ask him questions to get more information.
            Sometimes the user will directly prompt you with the result of a command.
        """,
        )
    ]
    """The conversation history."""

    def get(self) -> List[AIMessage]:
        """
        Return the conversation history.
        """
        return self.conversation

    def add(self, message: AIMessage) -> List[AIMessage]:
        """
        Add a message to the conversation history.
        """
        self.conversation.append(message)

        if len(self.conversation) > self.max_history:
            self.conversation.pop(0)

        return self.conversation

    def clear(self) -> List[AIMessage]:
        """
        Clear the conversation history.
        """
        self.conversation = []

        return self.conversation
