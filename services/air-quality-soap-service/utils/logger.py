"""
Configuration du système de logging
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
import uuid


def setup_logger(name: str, log_file: str, level=logging.INFO):
    """
    Configurer un logger avec rotation
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    handler.setFormatter(formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(console_handler)
    
    return logger


def get_request_logger(method: str, params: dict):
    """
    Logger avec contexte de requête
    """
    request_id = str(uuid.uuid4())[:8]
    logger = logging.getLogger(f'request.{method}')
    
    extra = {
        'request_id': request_id,
        'method': method,
        'params': params
    }
    
    return logging.LoggerAdapter(logger, extra)