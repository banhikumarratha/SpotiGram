import asyncio
import logging
from functools import wraps
from typing import Callable, Any, Type
import tenacity

logger = logging.getLogger(__name__)

def with_retry(
    max_attempts: int = 3,
    wait_multiplier: float = 1.0,
    wait_min: float = 1.0,
    wait_max: float = 10.0,
    retry_exceptions: tuple[Type[Exception], ...] = (Exception,),
):
    """
    Exponential backoff retry decorator using tenacity.
    """
    return tenacity.retry(
        stop=tenacity.stop_after_attempt(max_attempts),
        wait=tenacity.wait_exponential(multiplier=wait_multiplier, min=wait_min, max=wait_max),
        retry=tenacity.retry_if_exception_type(retry_exceptions),
        before_sleep=tenacity.before_sleep_log(logger, logging.WARNING)
    )

class CircuitBreakerOpenException(Exception):
    pass

def circuit_breaker(failure_threshold: int = 5, recovery_timeout: int = 30):
    """
    A simple async circuit breaker decorator.
    """
    def decorator(func: Callable) -> Callable:
        failures = 0
        last_failure_time = 0
        
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            nonlocal failures, last_failure_time
            
            # Check state
            if failures >= failure_threshold:
                time_since_failure = asyncio.get_event_loop().time() - last_failure_time
                if time_since_failure < recovery_timeout:
                    raise CircuitBreakerOpenException(f"Circuit breaker open for {func.__name__}")
                else:
                    # Half-open: allow one request to pass through
                    pass

            try:
                result = await func(*args, **kwargs)
                # Success: reset failures
                failures = 0
                return result
            except Exception as e:
                failures += 1
                last_failure_time = asyncio.get_event_loop().time()
                raise e

        return wrapper
    return decorator
