"""
Configuration du logger pour le microservice
"""
import logging
import sys
from pathlib import Path


def setup_logger(name: str = "urban-events-service", log_level: str = "INFO") -> logging.Logger:
    """
    Configure et retourne un logger
    
    Args:
        name: Nom du logger
        log_level: Niveau de log (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Logger configuré
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Ajout du handler
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger
