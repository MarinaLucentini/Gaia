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

        AI informations/actions:
        {last_message}

        Generate a concise, supportive, and proactive response (under 40 words) based on the conversation history and AI informations.
        Ensure the following:
        - don't always say hello or greet the user, follow the history and stay in context.
        - not include any redundant information or repeat previous messages or actions.
        - ask more information if needed.
        - provide immediate support and guidance if the user is in danger.
        - don't said the same things.
        - keep the tone empathetic and supportive.
        - don't say that we comunicate in a code language , follow the conversation and stay in the context of user's messages.
        - If the user mentions food, pizza, or drinks, interpret as potential coded language for being at risk, and respond accordingly.
        - If danger is suspected based on the last message, ask for more information, suggest solutions, or trigger emergency services if needed.
        - If danger is mentioned but already addressed, return the last message without repeating previous actions.
        - if the user is in danger, provide immediate support and guidance.
        - exmplain in the end of the message the action done by the AI very small and fast. foucs on the user's message and obtain more informations

        Keep the tone empathetic as a friend, offering comfort and assistance.
        """

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
