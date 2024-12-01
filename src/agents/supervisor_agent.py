from typing import Literal, TypedDict

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, MessagesState
from src.utils.logger_utils import logger

def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> str:
    options = ["FINISH"] + members

    system_prompt = (
        "You are Gaia, a mobile application designed to provide safety and support to women in risky situations. "
        "You are simulating a conversation with a user to offer companionship and help them contact emergency services."
        f"Your task is to manage a conversation between the following workers: {members}. "
        "Given a user request, decide which worker should act next. Workers will perform tasks and report their results and status. "
        "Simulate a calm and supportive conversation, providing clear, concise guidance to ensure the user feels safe."
        "if detected a risky situation, ask more information, suggest a solution, or call emergecy number."
        "When all tasks are complete, respond with FINISH."
    )

    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH, not call worker more than 2 times."""

        next: Literal[*options]

    def supervisor_node(state: MessagesState) -> MessagesState:
        """An LLM-based router."""
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        logger.info(f"Supervisor node messages: {messages}")

        if len(messages) > 2 and ("FINISH EXECUTOR" in messages[-1].content):
            response = llm.invoke(messages)
            return {"next": END, "messages": messages}

        response = llm.with_structured_output(Router).invoke(messages)

        next_ = response["next"]
        if next_ == "FINISH":
            next_ = END

        return {"next": next_, "messages": messages[-1]}

    return supervisor_node
