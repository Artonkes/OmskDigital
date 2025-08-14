from fastapi import HTTPException
from functools import wraps


def handle_error_500(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error is: {e}")
    return wrapper

