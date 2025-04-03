from functools import wraps
from fastapi import HTTPException, status
import logging

from httpx import HTTPStatusError

logger = logging.getLogger(__name__)

def handle_error(func):
    """
    Decorator to handle errors, log them, and raise appropriate HTTPException.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            logger.error(f"HTTP Exception: {e}", exc_info=e)
            raise e
        except HTTPStatusError as http:
            logger.error(f"HTTP Error: {http}", exc_info=http)
            raise HTTPException(
                status_code=http.response.status_code,
                detail=f"Failed to process request: {http}",
            )
        except Exception as e:
            logger.error(f"Unexpected Error: {e}", exc_info=e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {e}",
            )
    return wrapper