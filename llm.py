from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from typing import List, Optional, Literal
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import ToolMessage

from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage, trim_messages
from typing import TypedDict, Literal

from dotenv import load_dotenv
import os

# Carica le variabili dal file .env
load_dotenv()


chat = ChatGroq(
    temperature=0, groq_api_key=os.getenv("GROQ_API"), model_name="llama-3.1-70b-versatile"
)


def ask_question(question, chat):
    system = """
    You are Gaia is an innovative mobile empathic application designed to provide safety and support to women who find themselves alone in potentially risky situations. 
    The app simulates a empathic conversation with an AI to give the user the illusion of being in company, offering both emotional reassurance and a sense of security. 
    In addition, Gaia can help users call emergency services instantly if they are in danger. 

    The app also features a map that identifies the most dangerous areas based on real-time emergency call data, enabling users to avoid risky locations. 
    This data-driven approach will also assist law enforcement in intelligently focusing their efforts on areas with higher safety concerns.

    Simulate a phone empathic conversation with the user, being simple and concise. The goal is to provide immediate reassurance and support, ensuring the user feels safe and knows what to do in risky situations.
    """

    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | chat
    response = chain.invoke({"text": question})
    return response.content

def combine_question(history,last_message):
    key_meaning = (
        "Gaia is an innovative mobile empathic application designed to provide safety and support to women who find themselves alone in "
        "potentially risky situations. The app simulates a conversation with an AI to give the user the illusion of being in company, "
        "offering both emotional reassurance and a sense of security. In addition, Gaia can help users call emergency services instantly "
        "if they are in danger. The app also features a map that identifies the most dangerous areas based on real-time emergency call "
        "data, enabling users to avoid risky locations. This data-driven approach also assists law enforcement in focusing their efforts "
        "on areas with higher safety concerns."
    )
    
    prompt=   f"""
    You are Gaia, a mobile app designed to ensure the safety and well-being of women in potentially risky situations.  

    {key_meaning}

    Conversation history:

    {history}

    The last message sent by the AI:

    {last_message}

    Combine the conversation history and the last message to create a clear and helpful response for the user. Ensure:
    - Actions or steps described in the last message are included in the final response if they are not already present in the history.
    - Action as report or called emergency number are included in the response was make from the AI in background.
    - The response avoids redundancy and reflects the context of the user's situation.
    - If the user mentions food, pizza, or drinks, consider it might be coded language indicating they are under control or at risk, and respond accordingly.
    - The tone remains supportive, reassuring, and concise (under 60 words).

    Generate a logical, sensitive, empathic and proactive response that addresses the user's immediate needs.
    
    IF you think the {last_message} said a possible danger, in contrast to the previous messages, ask more information, suggest a solution, or call the emergency number.
    IF you think the {last_message} said a possible danger, return last_message without the action that he done in previous messages
    """

    response = chat.invoke(prompt)
    print(f"{response.content}")
    return response.content


def explain_action(actions: list[str]):
    """
    Create a response for chatbot for help people in danger.
    """

    system = """
        You are Gaia, a empathicmobile application designed to assist individuals in emergency situations by providing immediate support and guidance.
        If the situation requires, immediately instruct the user to send a report or call emergency services. 
        If these steps are taken, reassure the user by saying, "An operator will speak with you shortly." 
        Continue engaging with them, asking for more information if needed, and providing calming suggestions.
        Your goal is to keep the user calm, be empathic, offering helpful advice while they wait for emergency responders. 
        Your responses should be clear, concise (max 80 words), and empathetic, encouraging the user to stay engaged and share any additional details.

        Here's the conversation history with the user's messages and the action you took:
        """

    prompt = f"{system} AI Log and Actions Takenw without user of human:\n" + "\n".join(actions)

    response = chat.invoke(prompt)
    print(f"{response.content}")
    return response.content

@tool
def give_a_response(messages_of_request: list[str]):
    """
    Create a response for chatbot for help people in danger.
    """

    print(f"\t TOOL give_a_response : messages_of_request: {messages_of_request}")
    system = """
    You are Gaia, a mobile application designed to provide safety and support people.
    Help the people, ask more information, suggest a solution, or call emergecy number.
    imagine that you are like the emergency number. use coincidental answers max 50 words
    This is the history of the conversation and action:
    """

    prompt = f"{system} Log of hide actions:\n" + "\n".join(messages_of_request)

    response = chat.invoke(prompt)
    print(f"\t TOOL give_a_response : response: {response.content}")
    return response.content


@tool
def call_emergency(level_of_danger: int):
    """Call the emergency number only in situations of real danger,give a level from 0 to 3 of danger
    where 0 is not dangerous and 3 is very dangerous, 1 is maybe dangerous and 2 is probably dangerous"""
    print(f"\t TOOL call_emergency : level {level_of_danger} ")

    if level_of_danger==0:
        return "The situation is not dangerous"
    elif level_of_danger==1:
        return "We need more information about the situation"
    elif level_of_danger==2:
        return "We sent a report to the emergency number"
    else:
        return "Emergency number called"

@tool
def send_report():
    """Send a short report to the emergency number, if the situation is dangerous or suspicious"""
    print(f"\t TOOL send_report : Call emergency number called")

    return "save conversation and send report "


@tool
def calculate_food_and_drinks(
    num_people: int, food: list = None, drink_dict: dict = None
):
    """
    Detects unusual patterns in food or drink orders, returning the situation and number of people.
    """
    # Default values for food and drink_dict if not provided
    print(
        f"\t TOOL calculate_food_and_drinks :num_people: {num_people}, food: {food}, drink_dict: {drink_dict}"
    )
    food = food or {}
    drink_dict = drink_dict or {}

    # Potential danger scenarios based on food orders
    danger_scenarios = {
        "pizza": "Suspicious activity reported",
        "margherita": "Stalking or suspicious individual reported",
        "diavola": "Urgent help request",
        "hawaiian": "Immediate danger, call for help",
        "four cheese": "People trapped or blocked",
        "vegetarian": "Moderate danger, manageable situation",
    }

    # Determine the dangerous situation
    situation_description = []
    for food_item in food:
        if food_item.lower() in danger_scenarios:
            situation_description.append(f"{danger_scenarios[food_item]}")

    # If no dangerous situations are identified
    if not situation_description:
        situation_description = (
            "No dangerous situations detected. Ask to give more information"
        )

    # Output result
    result = {"num_people": num_people, "situations": situation_description}

    print(f"\t TOOL calculate_food_and_drinks : {result}")
    return f"There were this situation {result['situations']} and there are {result['num_people']} people, the person comunicated in code beacuse of the danger"


# The agent state is the input to each node in the graph
class AgentState(MessagesState):
    # The 'next' field indicates where to route to next
    next: str


def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> str:
    options = ["FINISH"] + members

    system_prompt = (
        "You are Gaia, a mobile application designed to provide safety and support to women in risky situations. "
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
        print(f"Supervisor node messages: {messages}")

        if len(messages) > 2 and ("FINISH EXECUTOR" in messages[-1].content):
            response = llm.invoke(messages)
            return {"next": END, "messages": messages}

        response = llm.with_structured_output(Router).invoke(messages)

        next_ = response["next"]
        if next_ == "FINISH":
            next_ = END

        return {"next": next_, "messages": messages[-1]}

    return supervisor_node


executor_agent = create_react_agent(
    chat,
    tools=[calculate_food_and_drinks, give_a_response, call_emergency, send_report],
)


def executor_node(state: AgentState) -> AgentState:
    result = executor_agent.invoke(state)
    
    tool_message_contents = [message.content for message in result['messages'] if isinstance(message, ToolMessage)]

    return {
        "messages": [
            AIMessage(
                content=explain_action(str(tool_message_contents)) + " FINISH EXECUTOR",
                name="language_in_code",
            )
        ]
    }


research_supervisor_node = make_supervisor_node(chat, ["executor"])

research_builder = StateGraph(MessagesState)
research_builder.add_node("supervisor", research_supervisor_node)
research_builder.add_node("executor", executor_node)
research_builder.add_edge(START, "supervisor")
research_builder.add_edge("executor", "supervisor")
research_builder.add_conditional_edges("supervisor", lambda state: state["next"])
research_graph = research_builder.compile()


def clear_messages_workflow(responses):
    all_messages = []
    for index, resp in enumerate(responses):
        if index == 0:
            prefix = "HumanMessage : "
        else:
            prefix = "AIMessage : "
        try:
            element = next(iter(resp.values()))["messages"]

            if isinstance(element, list):
                element = element[0].content
            else:
                element = element.content
            all_messages.append(prefix + element)
        except:
            pass

    return all_messages


def ask_gaia_with_tool(message: str):
    responses = []
    for s in research_graph.stream(
        {"messages": [("user", str(message))]},
        {"recursion_limit": 6},
    ):
        print(f"Main : {s}")
        responses.append(s)
        print("---")
    print("\n\n" + responses[-2]["executor"]["messages"][0].content)
    last_response = responses[-2]["executor"]["messages"][0].content
    
    print(f"History : {(message)}")
    
    if len(message) >1:
        combine_respoonde=combine_question(history=message, last_message=last_response[:-16])
        print(f"\n\nCombine : {combine_respoonde}\n\n")
        return responses, combine_respoonde
    else:
        return responses, last_response[:-16]
