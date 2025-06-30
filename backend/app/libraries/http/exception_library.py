from fastapi import HTTPException, status
from app.config.translations.i18n import get_translation

class ExceptionLibrary:
    @staticmethod
    def throw_404(instance, message_key="errors.record_not_found", locale="es", params=None):
        """
        Throws 404 if instance is None. Returns the instance if it exists.
        Args:
            instance: The instance to check.
            message_key: The key to use for the error message.
        Returns:
            The instance if it exists.
        Raises:
            HTTPException: If the instance is None.
        """
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_translation(message_key, locale=locale, **(params or {}))
            )
        return instance

    @staticmethod  
    def throw_404_if(condition, message_key="errors.record_not_found", locale="es", params=None):
        """
        Throws 404 if the condition is met.
        """
        if condition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=get_translation(message_key, locale=locale, **(params or {}))
            )

    @staticmethod   
    def throw_401(message_key="errors.unauthorized", locale="es", params=None):
        """
        Throws 401.
        Args:
            message_key: The key to use for the error message.
        Raises:
            HTTPException: If the condition is met.
        """
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=get_translation(message_key, locale=locale, **(params or {}))
        )

    @staticmethod
    def throw_401_if(condition, message_key="errors.unauthorized", locale="es", params=None):
        """
        Throws 401 if the condition is met.
        Args:
            condition: The condition to check.
            message_key: The key to use for the error message.
        Raises:
            HTTPException: If the condition is met.
        """
        if condition:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=get_translation(message_key, locale=locale, **(params or {}))
            )
            
    @staticmethod
    def throw_403(message_key="errors.forbidden", locale="es", params=None):
        """
        Throws 403.
        Args:
            message_key: The key to use for the error message.
        Raises:
            HTTPException: If the condition is met.
        """
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=get_translation(message_key, locale=locale, **(params or {}))
        )

    @staticmethod
    def throw_403_if(condition, message_key="errors.forbidden", locale="es", params=None):
        """
        Throws 403 if the condition is met.
        Args:
            condition: The condition to check.
            message_key: The key to use for the error message.
        Raises:
            HTTPException: If the condition is met.
        """
        if condition:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=get_translation(message_key, locale=locale, **(params or {}))
            )

    @staticmethod
    def throw_400(message_key="errors.bad_request", locale="es", params=None):
        """
        Throws 400.
        Args:
            message_key: The key to use for the error message.
        Raises:
            HTTPException: If the condition is met.
        """
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=get_translation(message_key, locale=locale, **(params or {}))
        )

    @staticmethod
    def throw_400_if(condition, message_key="errors.bad_request", locale="es", params=None):
        """
        Throws 400 if the condition is met.
        Args:
            condition: The condition to check.
            message_key: The key to use for the error message.
        Raises:
            HTTPException: If the condition is met.
        """
        if condition:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=get_translation(message_key, locale=locale, **(params or {}))
            )
            
    @staticmethod
    def throw_422(message_key="errors.unprocessable_entity", locale="es", params=None):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=get_translation(message_key, locale=locale, **(params or {}))
        )
        
    @staticmethod
    def throw_500_if(condition, message_key="errors.internal_server_error", locale="es", params=None):
        """
        Throws 500 if the condition is met.
        Args:
            condition: The condition to check.
            message_key: The key to use for the error message.
        Raises:
            HTTPException: If the condition is met.
        """
        if condition:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=get_translation(message_key, locale=locale, **(params or {}))
            ) 