# solvv_api/core/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
def start_scheduler():
    if not scheduler.running:
        scheduler.start()
