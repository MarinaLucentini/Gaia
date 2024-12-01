from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import create_react_agent

from src.agents.executor_agent import executor_node
from src.agents.supervisor_agent import make_supervisor_node
from src.tools.actions_tool import call_emergency, send_report
from src.tools.general_tool import calculate_food_and_drinks, give_a_response
from src.utils.call_llm_utils import combine_question,ask_question
from src.utils.llm_utils import chat
from src.utils.logger_utils import logger

research_supervisor_node = make_supervisor_node(chat, ["executor"])
research_builder = StateGraph(MessagesState)
research_builder.add_node("supervisor", research_supervisor_node)
research_builder.add_node("executor", executor_node)
research_builder.add_edge(START, "supervisor")
research_builder.add_edge("executor", "supervisor")
research_builder.add_conditional_edges("supervisor", lambda state: state["next"])
research_graph = research_builder.compile()


def ask_gaia_with_tool(message: str):
    responses = []
    for s in research_graph.stream(
        {"messages": [("user", str(message))]},
        {"recursion_limit": 6},
    ):
        responses.append(s)
        logger.debug(f"Responses: {s}")
    try:
        last_response = responses[-2]["executor"]["messages"][0].content[
            :-16
        ]  # remove " FINISH EXECUTOR"
        logger.info(f"last response executor: {last_response}")

        # if len(message) > 1:
        combine_respoonde = combine_question(
            history=message, informations=last_response
        )
        logger.info(f"Combine question: {last_response}")
        return responses, combine_respoonde
    except:
        last_response=ask_question(message)
        return responses, last_response
    # else:
    #     return responses, last_response
