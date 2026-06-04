from typing import Any, Dict

def sanitize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Utility function to sanitize payloads before logging or sending them.
    Masks common sensitive fields.
    """
    sensitive_keys = {"password", "token", "secret", "authorization"}
    sanitized = {}
    for k, v in payload.items():
        if any(sensitive in k.lower() for sensitive in sensitive_keys):
            sanitized[k] = "***MASKED***"
        else:
            sanitized[k] = v
    return sanitized
