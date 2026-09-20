import logging
import re
import sys


class PIIRedactionFilter(logging.Filter):
    """Logging filter to sanitize sensitive keys (passwords, tokens, API keys, secrets) from server logs."""

    SENSITIVE_PATTERNS = [
        (r'("password"\s*:\s*")([^"]+)(")', r'\1[REDACTED_PASSWORD]\3'),
        (r'("token"|"access_token"|"refresh_token"\s*:\s*")([^"]+)(")', r'\1[REDACTED_TOKEN]\3'),
        (r'("secret"|"api_key"|"secret_key"\s*:\s*")([^"]+)(")', r'\1[REDACTED_KEY]\3'),
        (r'(Bearer\s+)[A-Za-z0-9\-\._~\+\/]+=*', r'\1[REDACTED_BEARER_TOKEN]'),
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            for pattern, replacement in self.SENSITIVE_PATTERNS:
                record.msg = re.sub(pattern, replacement, record.msg, flags=re.IGNORECASE)
        return True


def setup_structured_logging():
    log_obj = logging.getLogger("agentx")
    log_obj.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [agentx] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    handler.addFilter(PIIRedactionFilter())

    if not log_obj.handlers:
        log_obj.addHandler(handler)

    return log_obj


logger = setup_structured_logging()
