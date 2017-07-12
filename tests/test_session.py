import asyncio
import json
import socket

import aiohttp
import aiohttp_mako
import aiohttp_session_flash
from aiohttp import web
from aiohttp_session_flash import flash, pop_flash
import pytest


def find_unused_port():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('127.0.0.1', 0))
	port = s.getsockname()[1]
	s.close()
	return port


def test_flash(app):
	
	async def test():
		handler = app.make_handler()
		port = find_unused_port()
		srv = await app.loop.create_server(handler, '127.0.0.1', port)
		url = "http://127.0.0.1:{}".format(port)

		async def json_context_processor(request):
			return {
				'json': lambda value: json.dumps(value)
			}

		lookup = aiohttp_mako.setup(app, context_processors=[aiohttp_session_flash.context_processor, json_context_processor])
		lookup.put_string('index.html', '${json(get_flashed_messages())}')
	
		async def save(request):
			flash(request, "Hello")
			return web.Response(body=b'OK')
		
		async def save_redirect(request):
			flash(request, "Redirect")
			raise web.HTTPFound('/')

		async def save_array(request):
			flash(request, ["This", "works", "too"])
			return web.Response(body=b'OK')

		async def show(request):
			return web.Response(body=json.dumps(pop_flash(request)).encode('utf-8'))
		
		@aiohttp_mako.template('index.html')
		async def show_context_processor(request):
			return {}
		
		app.router.add_route('GET', '/save', save)
		app.router.add_route('GET', '/save_redirect', save_redirect)
		app.router.add_route('GET', '/save_array', save_array)
		app.router.add_route('GET', '/show', show)
		app.router.add_route('GET', '/show_context_processor', show_context_processor)
	
		with aiohttp.ClientSession() as session:
			async with session.get(url+'/save') as resp:
				assert resp.status == 200

			async with session.get(url+'/save_redirect', allow_redirects=False) as resp:
				assert resp.status == 302

			async with session.get(url+'/save_array') as resp:
				assert resp.status == 200
	
			async with session.get(url+'/show') as resp:
				assert resp.status == 200
				assert (await resp.text()) == '["Hello", "Redirect", ["This", "works", "too"]]'

			async with session.get(url+'/show') as resp:
				assert resp.status == 200
				assert (await resp.text()) == '[]'

			async with session.get(url+'/save') as resp:
				assert resp.status == 200

			async with session.get(url+'/show_context_processor') as resp:
				assert resp.status == 200
				assert (await resp.text()) == '["Hello"]'

	app.loop.run_until_complete(test())
