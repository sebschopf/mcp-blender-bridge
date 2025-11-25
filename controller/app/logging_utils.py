import json
import logging
import time
from typing import Optional

# Standard format for log entries to make them easily parsable
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class JsonFormatter(logging.Formatter):
    """Formatter that outputs JSON strings after the standard log prefix.
    Useful for structured logging if needed, though simple text tagging is often enough for debugging.
    """

    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # If extra fields were passed
        if hasattr(record, "duration"):
            log_record["duration"] = record.duration
        if hasattr(record, "tag"):
            log_record["tag"] = record.tag

        return json.dumps(log_record)


class PerformanceLogger:
    """Context manager for tracking duration of operations and logging start/end events with precise timestamps.

    Usage:
        with PerformanceLogger("TAG_NAME", "Operation description") as pl:
            # do something
    """

    def __init__(self, tag: str, message: str = "", logger: Optional[logging.Logger] = None):
        self.tag = tag
        self.message = message
        self.logger = logger or logging.getLogger("performance")
        self.start_time = 0.0

    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(f"[{self.tag}_START] {self.message}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        duration = end_time - self.start_time
        status = "FAILED" if exc_type else "SUCCESS"

        log_msg = f"[{self.tag}_END] {self.message} - Status: {status} - Duration: {duration:.4f}s"

        if exc_type:
            self.logger.error(log_msg, exc_info=(exc_type, exc_val, exc_tb))
        else:
            self.logger.info(log_msg)
