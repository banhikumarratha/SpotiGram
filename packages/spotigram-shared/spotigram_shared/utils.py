def format_response(status: str, data: dict = None, message: str = None) -> dict:
    return {
        "status": status,
        "data": data or {},
        "message": message or ""
    }
