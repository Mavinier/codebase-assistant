import logging

from codebase_assistant.config.settings import settings


def setup_logging() -> None:
    logging.basicConfig(
        level=settings.log_level.upper(),
        format=("%(asctime)s | %(levelname)s | %(name)s | %(message)s"),
    )
