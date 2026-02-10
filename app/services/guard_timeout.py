import asyncio
from app.core.config import FRAGMENT_GUARD_TIMEOUT

# sender -> asyncio.Task
_GUARD_TASKS = {}


def cancel_guard_timeout(sender: str):
    task = _GUARD_TASKS.pop(sender, None)
    if task and not task.done():
        task.cancel()


async def schedule_guard_timeout(sender: str, send_clarification):
    async def _wait_and_fire():
        try:
            await asyncio.sleep(FRAGMENT_GUARD_TIMEOUT)
            await send_clarification(sender)
        except asyncio.CancelledError:
            pass
        finally:
            _GUARD_TASKS.pop(sender, None)

    cancel_guard_timeout(sender)
    _GUARD_TASKS[sender] = asyncio.create_task(_wait_and_fire())
