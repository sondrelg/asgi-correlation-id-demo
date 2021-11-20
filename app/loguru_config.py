import logging
import sys

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from loguru import logger


def configure_logging():
    from asgi_correlation_id.context import correlation_id

    def correlation_id_filter(record):
        record['correlation_id'] = correlation_id.get()
        return record['correlation_id']

    logger.remove()
    fmt = "{level}: \t  {time} {name}:{line} [{correlation_id}] - {message}"
    logger.add(sys.stderr, format=fmt, level=logging.DEBUG, filter=correlation_id_filter)


app = FastAPI(on_startup=[configure_logging])
app.add_middleware(CorrelationIdMiddleware)


@app.get('/')
def index():
    logger.info('Log with correlation ID')
