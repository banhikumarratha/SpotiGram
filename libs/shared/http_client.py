import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# We can mock circuit breaker state using a simple global variable or a library like circuitbreaker
class CircuitBreakerOpenException(Exception):
    pass

def http_get_with_retry(url: str, timeout: int = 5):
    """
    HTTP GET with exponential backoff retries.
    """
    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((requests.exceptions.RequestException, CircuitBreakerOpenException))
    )
    def _execute():
        # Insert circuit breaker check here in a real lib
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp
        
    return _execute()
