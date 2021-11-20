import logging
from logging.config import dictConfig

from asgi_correlation_id import correlation_id_filter, CorrelationIdMiddleware
from fastapi import FastAPI

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'filters': {
                'correlation_id': {'()': correlation_id_filter(32)},
            },
            'formatters': {
                'console': {
                    'class': 'logging.Formatter',
                    'datefmt': '%H:%M:%S',
                    'format': '%(levelname)s: \t  %(asctime)s %(name)s:%(lineno)d [%(correlation_id)s] %(message)s',
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'filters': ['correlation_id'],
                    'formatter': 'console',
                },
            },
            'loggers': {
                # project
                'app': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
                # third-party packages
                'httpx': {'handlers': ['console'], 'level': 'INFO'},
                'databases': {'handlers': ['console'], 'level': 'WARNING'},
                'asgi_correlation_id': {'handlers': ['console'], 'level': 'WARNING'},
            },
        }
    )


app = FastAPI(on_startup=[configure_logging])
app.add_middleware(CorrelationIdMiddleware)


@app.get('/')
def index():
    logger.info('Log with correlation ID')
