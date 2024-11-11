import uuid
from typing import List, TypedDict

from langchain_cohere import ChatCohere
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    ToolMessage,
)
from pydantic import BaseModel

from hackathon.settings import get_settings

settings = get_settings()


class Example(TypedDict):
    """A representation of an example consisting of text input and expected
     tool calls.

    For extraction, the tool calls are represented as instances of pydantic
    model.
    """

    input: str
    tool_calls: List[BaseModel]


def tool_example_to_messages(example: Example) -> List[BaseMessage]:
    """Convert an example into a list of messages that can be fed into an LLM.

    This code is an adapter that converts our example to a list of messages
    that can be fed into a chat model.

    The list of messages per example corresponds to:

    1) HumanMessage: contains the content from which content should be
    extracted.
    2) AIMessage: contains the extracted information from the model
    3) ToolMessage: contains confirmation to the model that the model requested
    a tool correctly.

    The ToolMessage is required because some of the chat models are
    hyper-optimized for agents rather than for an extraction use case.
    """
    messages: List[BaseMessage] = [HumanMessage(content=example['input'])]

    tool_calls = []

    for tool_call in example['tool_calls']:
        tool_calls.append(
            {
                'id': str(uuid.uuid4()),
                'args': tool_call.model_dump(),
                # The name of the function right now corresponds
                # to the name of the pydantic model
                # This is implicit in the API right now,
                # and will be improved over time.
                'name': tool_call.__class__.__name__,
            },
        )

    messages.append(AIMessage(content='', tool_calls=tool_calls))

    tool_outputs = example.get('tool_outputs') or [
        'You have correctly called this tool.'
    ] * len(tool_calls)

    for output, tool_call in zip(tool_outputs, tool_calls):
        messages.append(
            ToolMessage(content=output, tool_call_id=tool_call['id'])
        )

    return messages


def get_llm():
    llm = ChatCohere(
        model='command-r-plus', cohere_api_key=settings.COHERE_API_KEY
    )

    return llm
