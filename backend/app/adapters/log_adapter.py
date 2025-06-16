from loguru import logger
from typing import Any, Dict, Optional

class LogAdapter:

    
    @staticmethod
    def _build_context_msg(message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Build the context message for the log.
        """
        if context:
            context_str = " | " + " | ".join(f"{k}={v}" for k, v in context.items())
            return f"{message}{context_str}"
        return message

    @staticmethod
    def debug(message: str, context: Optional[Dict[str, Any]] = None):
        logger.debug(LogAdapter._build_context_msg(message, context))

    @staticmethod
    def info(message: str, context: Optional[Dict[str, Any]] = None):
        logger.info(LogAdapter._build_context_msg(message, context))

    @staticmethod
    def warning(message: str, context: Optional[Dict[str, Any]] = None):
        logger.warning(LogAdapter._build_context_msg(message, context))

    @staticmethod
    def error(message: str, context: Optional[Dict[str, Any]] = None):
        logger.error(LogAdapter._build_context_msg(message, context))

    @staticmethod
    def exception(message: str, context: Optional[Dict[str, Any]] = None):
        logger.exception(LogAdapter._build_context_msg(message, context))
        
    @staticmethod
    def critical(message: str, context: Optional[Dict[str, Any]] = None):
        logger.critical(LogAdapter._build_context_msg(message, context))
        
        
        
        