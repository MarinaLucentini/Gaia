from langchain_core.tools import tool
from src.utils.logger_utils import logger

@tool
def give_a_response(messages_of_request: list[str], chat):
    """
    Create a response for chatbot for help people in danger.
    """

    logger.info(f"\t TOOL give_a_response : messages_of_request: {messages_of_request}")
    system = """
    You are Gaia, a mobile application designed to provide safety and support to people.
    Your goal is to assist users in emergencies or difficult situations by asking for more information, suggesting solutions, or calling the emergency number if necessary.
    Respond to the user in a friendly and caring tone, asking for details to better understand the situation, and provide solutions or next steps.
    Imagine you are similar to an emergency number operator, so be compassionate, concise, and direct.
    
    Message of user : {messages_of_request}
    
    If the user's message is unclear, kindly ask for more details in a short and friendly manner, such as:
    
    - "I m not sure I understand. Can you tell me more about what s happening?"
    - "Could you explain what s going on a bit more?"
    - "Can you share a bit more about what you need help with?"
    - "Who are you and what s the situation? I want to help!"
    
    Always aim to clarify the situation and provide the most relevant advice or next steps. Keep responses brief, under 50 words.
    """

    prompt = f"{system} Log of hide actions:\n" + "\n".join(messages_of_request)

    response = chat.invoke(prompt)
    logger.info(f"\t TOOL give_a_response : response: {response.content}")
    return response.content


@tool
def calculate_food_and_drinks(
    num_people: int, food: list = None, drink_dict: dict = None
):
    """
    Take information about food and drinks or food desired for logger
    """
    # Default values for food and drink_dict if not provided
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

    situation_description = []
    
    for food_scen in list(danger_scenarios.keys()):
        if food_scen.lower() in str(food).lower():
            situation_description.append(danger_scenarios[food_scen])
            
    situation_description=list(set(situation_description))
    
    # If no dangerous situations are identified
    if not situation_description:
        situation_description = (
            "No dangerous situations detected. Ask to give more information"
        )

    # Output result
    result = {"num_people": num_people, "situations": situation_description}

    logger.info(f"\t TOOL calculate_food_and_drinks : {result}")
    return f"There were this situation {result['situations']} and there are {result['num_people']} people, the person comunicated in code beacuse of the danger"
