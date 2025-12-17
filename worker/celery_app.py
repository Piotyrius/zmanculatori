from __future__ import annotations

import os

from celery import Celery


CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", CELERY_BROKER_URL)

celery_app = Celery(
    "garment_pattern_worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

celery_app.conf.task_queues = {
    "high_priority": {"exchange": "high_priority", "routing_key": "high_priority"},
    "standard": {"exchange": "standard", "routing_key": "standard"},
    "low": {"exchange": "low", "routing_key": "low"},
}






