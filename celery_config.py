# celery_config.py

from kombu import Exchange, Queue

# celery_config.py

CELERY_BROKER_URL = 'memory://localhost/'

CELERY_RESULT_BACKEND = 'rpc://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_DISABLE_RATE_LIMITS = True

CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
)

CELERY_IMPORTS = ('tasks', )
