import asyncio

from src.tracker import Tracker

if __name__ == '__main__':
    tracker = Tracker()
    asyncio.run(
        tracker.run()
    )

