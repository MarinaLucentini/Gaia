from langchain_core.prompts import ChatPromptTemplate

from src.utils.llm_utils import chat
from src.utils.logger_utils import logger

def ask_question(question):
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


def combine_question(history, last_message):
    key_meaning = (
            "Gaia is a mobile app designed to provide safety and support to women in potentially risky situations. "
            "It simulates an AI conversation for emotional reassurance and a sense of security. "
            "Gaia also allows users to call emergency services instantly, and features a map highlighting dangerous areas "
            "based on real-time emergency data. This helps users avoid risky locations and assists law enforcement in targeting areas "
            "with higher safety concerns. Additionally, Gaia can serve as a virtual companion, offering a feeling of presence and support."
        )
    
    
    prompt = f"""
        You are Gaia, a mobile app designed to ensure the safety and well-being of women in potentially risky situations.

        {key_meaning}

        Conversation history:
        {history}

        Last AI message:
        {last_message}

        Generate a concise, supportive, and proactive response (under 60 words) based on the conversation history and last message. Ensure the following:
        - Include actions from the last message if not already present.
        - Mention any background actions like emergency calls or reports made by the AI.
        - Avoid redundancy and reflect the user's context.
        - If the user mentions food, pizza, or drinks, interpret as potential coded language for being at risk, and respond accordingly.
        - If danger is suspected based on the last message, ask for more information, suggest solutions, or trigger emergency services if needed.
        - If danger is mentioned but already addressed, return the last message without repeating previous actions.

        Ensure the tone remains empathetic and clear.
        """

    response = chat.invoke(prompt)
    logger.info(f"{response.content}")
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

    prompt = f"{system} AI Log and Actions Takenw without user of human:\n" + "\n".join(
        actions
    )

    response = chat.invoke(prompt)
    logger.info(f"{response.content}")
    return response.content
