import asyncio

from aiohttp import web
import aiohttp_session
import aiohttp_session_flash
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import pytest


@pytest.yield_fixture
def loop():
	# Set-up
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	yield loop

	# Clean-up
	loop.close()


@pytest.yield_fixture
def app(loop):
	app = web.Application(
		loop=loop,
		middlewares=[
			aiohttp_session.session_middleware(EncryptedCookieStorage(b'x'*32)),
			aiohttp_session_flash.middleware,
		]
	)
	yield app
	loop.run_until_complete(app.shutdown())
	loop.run_until_complete(app.cleanup())
	loop.close()
