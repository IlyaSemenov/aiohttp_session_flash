aiohttp_session_flash
=====================

The library provides flash messages for `aiohttp.web`_ on top of `aiohttp_session`_.

.. _aiohttp.web: https://aiohttp.readthedocs.io/en/latest/web.html
.. _aiohttp_session: https://github.com/aio-libs/aiohttp_session

“Flash messages” are simply a queue of string messages (or other JSON-serializable objects) stored in the session.


Usage
=====

Add `session_middleware` and `aiohttp_session_flash.middleware` to the list of `app`'s middleware:

.. code:: python

	app = web.Application(
		middlewares=[
			aiohttp_session.session_middleware(EncryptedCookieStorage(b'x'*32)),
			aiohttp_session_flash.middleware,
		]
	)

Within the handler, pull and push flash messages as needed:

.. code:: python

	from aiohttp import web

	from aiohttp_session_flash import flash, pop_flash


	async def foo(request):
		flash(request, "Hello")
		flash(request, ["This", "works", "too"])
		return web.Response(body=b'Flashed some messages')

	async def bar(request):
		for message in pop_flash(request):
			print(message)
		return web.Response(body=b'OK')


Template context processor
--------------------------

The template context processor is provided for template libraries that can use it:

.. code:: python

	aiohttp_mako_context_processors.setup(app, [
		...
		aiohttp_session_flash.context_processor,
	])

.. code:: mako

	<ul>
	% for message in get_flashed_messages():
		<li>${message}</li>
	% endfor
	</ul>
