# app/core/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()

def setup_scheduler(jobs: list[tuple]):
    """
    Registra los jobs en el scheduler.
    Cada job es una tupla (func, cron_kwargs).
    """
    for func, cron_kwargs in jobs:
        scheduler.add_job(func, CronTrigger(**cron_kwargs))
