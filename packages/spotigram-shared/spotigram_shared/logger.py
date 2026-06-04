import logging
from spotigram_config import settings
import json

# Minimal OpenTelemetry stub for structured logging and trace injection
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "trace_id": getattr(record, "trace_id", "00000000000000000000000000000000"),
            "span_id": getattr(record, "span_id", "0000000000000000")
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        # Use structured JSON formatter for Observability-First Development
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(level)
    return logger
