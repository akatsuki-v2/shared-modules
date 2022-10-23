from __future__ import annotations

import logging as stdlib_logging
import os
from contextvars import ContextVar
from typing import Any

import structlog
from structlog.types import EventDict
from structlog.types import WrappedLogger

_ROOT_LOGGER = stdlib_logging.getLogger("service-root")

_REQUEST_ID_CONTEXT = ContextVar("request_id")


def set_request_id(request_id: str | None) -> None:
    _REQUEST_ID_CONTEXT.set(request_id)


def get_request_id() -> Any | None:
    return _REQUEST_ID_CONTEXT.get(None)


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    return structlog.wrap_logger(_ROOT_LOGGER, logger_name=name or "root")


def log_as_text(app_env: str) -> bool:
    return app_env == "local"


def add_process_id(_: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
    event_dict["process_id"] = os.getpid()
    return event_dict


def add_request_id(_: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
    if request_id := _REQUEST_ID_CONTEXT.get(None):
        event_dict["request_id"] = request_id

    return event_dict


def configure_logging(app_env: str, log_level: str | int) -> None:
    if log_as_text(app_env):
        renderer = structlog.dev.ConsoleRenderer(colors=True)
    else:
        renderer = structlog.processors.JSONRenderer()

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=[
            structlog.processors.TimeStamper(fmt="iso", key="timestamp"),
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            add_process_id,
            add_request_id,
        ],
    )

    handler = stdlib_logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(log_level)

    # brute force control of the message format & level
    # TODO: loggers can be created after this. how should we handle that?
    existing_loggers = [
        stdlib_logging.getLogger(name)
        for name in stdlib_logging.root.manager.loggerDict
    ]
    for logger in existing_loggers:
        logger.handlers = []
        logger.addHandler(handler)
        logger.setLevel(log_level)


def debug(*args, **kwargs) -> None:
    return get_logger().debug(*args, **kwargs)


def info(*args, **kwargs) -> None:
    return get_logger().info(*args, **kwargs)


def warning(*args, **kwargs) -> None:
    return get_logger().warning(*args, **kwargs)


def error(*args, **kwargs) -> None:
    return get_logger().error(*args, **kwargs)


def critical(*args, **kwargs) -> None:
    return get_logger().critical(*args, **kwargs)