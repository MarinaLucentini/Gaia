from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.prebuilt import create_react_agent

from src.models.state_model import AgentState
from src.tools.actions_tool import call_emergency, send_report
from src.tools.general_tool import calculate_food_and_drinks, give_a_response
from src.utils.call_llm_utils import explain_action
from src.utils.llm_utils import chat
from src.utils.logger_utils import logger

executor_agent = create_react_agent(
    chat,
    tools=[calculate_food_and_drinks, call_emergency, send_report],
)


def executor_node(state: AgentState) -> AgentState:
    result = executor_agent.invoke(state)

    logger.debug(f"Executor node result {str(result)}")

    tool_message_contents=[]
    for message in result["messages"]:
        if isinstance(message, ToolMessage) and ("error" not in message.content.lower()):
            logger.info(f"\tExecutor node {message.name} message: {message.content}")
            tool_message_contents.append(message.content)
            
    result_action = explain_action(str(tool_message_contents))

    logger.info(f"Executor node result action: {result_action}")

    return {
        "messages": [
            AIMessage(
                content=result_action + " FINISH EXECUTOR",
                name="language_in_code",
            )
        ]
    }
