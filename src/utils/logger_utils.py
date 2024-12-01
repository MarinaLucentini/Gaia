import logging
from functools import wraps

# Configurazione di base del logger
logging.basicConfig(
    level=logging.INFO,  # Livello del logger
    format="%(funcName)s - %(lineno)d - %(message)s",  # Mostra la funzione e il numero di riga
    datefmt="%Y-%m-%d %H:%M:%S",  # Formato della data
)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
