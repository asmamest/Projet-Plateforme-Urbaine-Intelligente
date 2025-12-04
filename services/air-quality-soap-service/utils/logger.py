"""
Configuration du logging avec rotation
"""
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

def setup_logger(name: str = "air-quality-soap", log_level: str = "INFO"):
    """
    Configure le logger avec rotation de fichiers
    """
    # Créer le dossier logs s'il n'existe pas
    os.makedirs("logs", exist_ok=True)
    
    # Configuration du logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler pour fichier avec rotation
    file_handler = RotatingFileHandler(
        'logs/service.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler pour console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Logger par défaut
logger = setup_logger()
