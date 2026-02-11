import asyncio
from app.services.conversation import pop_if_stable
from app.core.config import DEBOUNCE_SECONDS

_PENDING = {}

async def schedule(sender: str, on_fire):
    async def _wait():
        try:
            print("DEBOUNCE START for", sender)
            await asyncio.sleep(DEBOUNCE_SECONDS)
            print("DEBOUNCE WAKE for", sender)

            messages = pop_if_stable(sender, DEBOUNCE_SECONDS)
            print("POP RESULT:", messages)

            if messages:
                await on_fire(sender, messages)
            else:
                print("NOT STABLE YET")
        except asyncio.CancelledError:
            print("DEBOUNCE CANCELLED for", sender)
            return

    task = _PENDING.get(sender)
    if task and not task.done():
        task.cancel()

    _PENDING[sender] = asyncio.create_task(_wait())
