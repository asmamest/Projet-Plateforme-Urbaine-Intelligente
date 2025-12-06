"""
Configuration du logger avec format JSON structuré
"""
import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logger(name: str, level: int = logging.INFO):
    """
    Configure un logger avec format JSON structuré
    
    Args:
        name: Nom du logger
        level: Niveau de log (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Format JSON structuré
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger