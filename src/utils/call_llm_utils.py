from langchain_core.prompts import ChatPromptTemplate

from src.utils.llm_utils import chat
from src.utils.logger_utils import logger

def ask_question(history):
    prompt = """
        You are Gaia, an innovative mobile empathic application designed to provide safety and support to women who find themselves alone in potentially risky situations. 
        The app simulates an empathic conversation with an AI to give the user the illusion of being in company, offering both emotional reassurance and a sense of security. 
        In addition, Gaia can help users call emergency services instantly if they are in danger. 

        The app also features a map that identifies the most dangerous areas based on real-time emergency call data, enabling users to avoid risky locations. 
        This data-driven approach will also assist law enforcement in intelligently focusing their efforts on areas with higher safety concerns.

        Simulate a phone empathic conversation with the user, being simple and concise. The goal is to provide immediate reassurance and support, ensuring the user feels safe and knows what to do in risky situations.

        If nothing else has occurred, send a message reassuring the user that everything is okay, authorities have been alerted, and the situation is resolved, but they may be contacted for follow-up.

        Give a short response from this history (max 30 words):
        {history}
        """
    
    response = chat.invoke(prompt)
    return response.content


def combine_question(history, informations):
    key_meaning = (
        "Gaia is a mobile app designed for women's safety, offering emotional reassurance and real-time support. "
        "It can call emergency services, highlight risky areas, and provide a feeling of presence. Gaia helps users avoid dangerous places, "
        "assist law enforcement, and provide virtual companionship."
    )

    logger.info(f"\n AI ACTION: {informations}\n")
    prompt = f"""
    {key_meaning}

    Conversation history:
    {history}

    AI information/actions:
    {informations}
    Insert this information if called or reported and suggest solutions.

    Generate a concise, supportive response (under 50 words) explaining the action and information extracted, with a respectful and professional tone. Ensure the following:
    - Stay in context, avoid unnecessary greetings or repeating messages.
    - Don't repeat previous actions or say "hello," "hi," or similar phrases like "I'm here to help..."
    - Provide immediate support if the user is in danger.
    - Maintain a tone that is empathetic and family-like, but without using informal or overly affectionate language.
    - If a report or emergency call was made, mention it if not in history.

    Keep the tone respectful, comforting, and helpful.
    """
    logger.info(f"UPDATE 2")
    response = chat.invoke(prompt)
    logger.info(f"{response.content}")
    return response.content


def explain_action(actions: list[str]):
    """
    Create a response for chatbot for help people in danger.
    """

    system = """
        Explain the situation or the action done by the AI to the user in a clear and concise manner.
        return a message of description information or action, the message should be under 30 words.
        the message should be clear and concise, and should not contain any redundant information.
        """

    prompt = f"{system} Information extract by AI or action :\n" + "\n".join(
        actions
    )

    response = chat.invoke(prompt)
    logger.info(f"{response.content}")
    return response.content
