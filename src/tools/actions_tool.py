from langchain_core.tools import tool
from src.utils.logger_utils import logger

@tool
def call_emergency(level_of_danger: int):
    """Call the emergency number only in situations of real danger,give a level from 0 to 3 of danger
    where 0 is not dangerous and 3 is very dangerous, 1 is maybe dangerous and 2 is probably dangerous
    """
    logger.info(f"\t TOOL call_emergency : level {level_of_danger} ")

    if level_of_danger == 0:
        return "The situation is not dangerous"
    elif level_of_danger == 1:
        return "We need more information about the situation"
    elif level_of_danger == 2:
        return "We sent a report to the emergency number"
    else:
        return "Emergency number called"


@tool
def send_report():
    """Send a short report to the emergency number, if the situation is dangerous or suspicious"""
    logger.info(f"\t TOOL send_report ")

    return "save conversation and send a report"
