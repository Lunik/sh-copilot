"""
OpenAI model
"""

from typing import ClassVar, Optional, Any, List, Dict

from pydantic import model_validator

from sh_copilot.ai.models.base import BaseAIModel
from sh_copilot.ai.context import AIContext, AIMessage, AIAuthorType, ChunkedAIMessage


class OpenAIModel(BaseAIModel):
    """
    OpenAI model
    """

    name: ClassVar[str] = "openai"
    """Name of the model."""

    engine: Any = None
    """Engine of the model."""

    api_type: str = "openai"
    """Type of the API used by the model. Can be 'openai', 'azure' or 'azure_ad'."""

    api_base: Optional[str] = None
    """Base URL of the API."""

    api_version: Optional[str] = None
    """Version of the API."""

    api_key: Optional[str] = None
    """API key."""

    deployment: Optional[str]
    """Deployment of the model."""

    deployment_kwargs: Optional[Dict[str, Any]] = {
        "temperature": 0.7,
        "max_tokens": 800,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": None,
    }

    @model_validator(mode="after")
    def init_model(cls, values):  # pylint: disable=no-self-argument
        """
        Initialize the model.
        """

        try:
            import openai  # pylint: disable=import-outside-toplevel

            values.engine = openai.ChatCompletion
        except ImportError as error:
            raise ModuleNotFoundError(
                "Could not import openai python package. "
                "Please install it with `pip install sh-copilot[openai]`."
            ) from error

        openai.api_type = values.api_type
        openai.api_base = values.api_base
        openai.api_version = values.api_version

        if values.api_type == "azure_ad":
            # If the API type is Azure AD, we need to use the azure-identity package to get a token.
            try:
                from azure.identity import (  # pylint: disable=import-outside-toplevel
                    DefaultAzureCredential,
                )
            except ImportError as error:
                raise ModuleNotFoundError(
                    "Could not import azure-identity python package. "
                    "Please install it with `pip install sh-copilot[azure]`."
                ) from error

            credential = DefaultAzureCredential()
            openai.api_key = credential.get_token(
                "https://cognitiveservices.azure.com"
            ).token
        else:
            # Otherwise, we can use the API key directly.
            openai.api_key = values.api_key

        return values

    def parse_context(self, context: AIContext) -> List[Dict[str, str]]:
        """
        Parse the context to a list of dict.
        """
        conversation = []
        for message in context.get():
            if message.author == AIAuthorType.HUMAN:
                conversation.append({"role": "user", "content": message.content})
            else:
                conversation.append({"role": "assistant", "content": message.content})

        return conversation

    def chat_completion(self, context: AIContext) -> AIMessage:
        """
        Return a OpenAI response.
        """
        conversation = self.parse_context(context)

        response = self.engine.create(
            engine=self.deployment, messages=conversation, **self.deployment_kwargs
        )

        message = response["choices"][0]["message"]

        return AIMessage(content=message["content"], author=AIAuthorType.AI)

    def chat_completion_stream(self, context: AIContext) -> ChunkedAIMessage:
        """
        Return a OpenAI response stream.
        """
        conversation = self.parse_context(context)

        response = self.engine.create(
            stream=True,
            engine=self.deployment,
            messages=conversation,
            **self.deployment_kwargs
        )

        for chunk in response:
            if len(chunk["choices"]) == 0:
                continue

            delta = chunk["choices"][0]["delta"]
            yield ChunkedAIMessage(
                content=delta.get("content", ""), author=AIAuthorType.AI
            )
