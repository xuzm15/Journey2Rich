from __future__ import annotations

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from journey2rich.config import get_settings
from journey2rich.engine.push import run_push


def run_daily_scheduler() -> None:
    settings = get_settings()
    scheduler = BlockingScheduler(timezone=settings.timezone)
    trigger = CronTrigger(hour=8, minute=0, timezone=settings.timezone)
    scheduler.add_job(run_push, trigger=trigger, id="daily_push", replace_existing=True)
    scheduler.start()
