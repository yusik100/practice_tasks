import asyncio
from typing import Any, Callable, List, Optional

class AsyncArrayVariants:
    def __init__(
        self,
        items: List[Any],
        cancel_event: Optional[asyncio.Event] = None
    ):
        self.items = items
        self.cancel_event = cancel_event

    def callback_map(
        self,
        async_fn: Callable[[Any, int], Any],
        callback: Callable[[List[Any]], None],
        err_callback: Optional[Callable[[Exception], None]] = None
    ) -> None:
        results: List[Any] = [None] * len(self.items)
        pending = len(self.items)

        def _maybe_done():
            nonlocal pending
            pending -= 1
            if pending == 0:
                callback(results)

        for idx, item in enumerate(self.items):
            if self.cancel_event and self.cancel_event.is_set():
                if err_callback:
                    err_callback(asyncio.CancelledError())
                return

            async def _run(i, x):
                nonlocal results
                try:
                    res = await async_fn(x, i)
                    results[i] = res
                except Exception as e:
                    if err_callback:
                        err_callback(e)
                    return
                _maybe_done()

            asyncio.create_task(_run(idx, item))

    def promise_map(self, async_fn: Callable[[Any, int], Any]) -> asyncio.Task:
        async def _worker():
            results: List[Any] = []
            for idx, item in enumerate(self.items):
                if self.cancel_event and self.cancel_event.is_set():
                    raise asyncio.CancelledError()
                res = await async_fn(item, idx)
                results.append(res)
            return results

        return asyncio.create_task(_worker())