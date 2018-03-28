
import aiohttp
import asyncio
import logging
import os

from guillotina import configure

from guillotina_linkchequer.content import check_item
from guillotina_linkchequer.interfaces import ILinkChecker

logger = logging.getLogger("linkchequer")

IS_WORKER = os.getenv("IS_WORKER", None)


@configure.utility(provides=ILinkChecker)
class LinkCheckerUtility:

    def __init__(self, settings=None, loop=None):
        self._loop = loop
        self._settings = settings
        self._scheduled = dict()

    async def initialize(self, app=None):

        if not IS_WORKER:
            return

        db = app.root['db']
        tm = db.get_transaction_manager()
        txn = await tm.begin()
        container = await db.async_get('container')
        links = await container.async_get('links')
        if not self._loop:
            self._loop = asyncio.get_event_loop()

        async for item in links.async_values():
            tc = await item.next_tick()
            logger.debug(f'scheduling {item.url} at {tc}')
            # todo lock this instance as the only worker
            hand = self._loop.call_later(
                tc, lambda: asyncio.ensure_future(check_item(item))
            )
            self._scheduled[item.id] = hand

        await tm.abort(txn=txn)

    async def add(self, item):

        if item.id in self._scheduled:
            self._scheduled[item.id].cancel()

        nt = await item.next_tick()
        logger.debug(f'scheduling {item.url} when {nt}')
        hand = self._loop.call_later(
            nt, lambda: asyncio.ensure_future(check_item(item))
        )
        self._scheduled[item.id] = hand

    async def remove(self, item):
        if item.id in self._scheduled:
            self._scheduled[item.id].cancel()
            del self._scheduled[item.id]
