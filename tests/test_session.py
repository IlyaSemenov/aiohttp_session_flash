import asyncio
import json
import socket

import aiohttp
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
			return web.Response(body="|".join(map(json.dumps, pop_flash(request))).encode('utf-8'))
		
		app.router.add_route('GET', '/save', save)
		app.router.add_route('GET', '/save_redirect', save_redirect)
		app.router.add_route('GET', '/save_array', save_array)
		app.router.add_route('GET', '/show', show)
	
		with aiohttp.ClientSession() as session:
			async with session.get(url+'/save') as resp:
				assert resp.status == 200

			async with session.get(url+'/save_redirect', allow_redirects=False) as resp:
				assert resp.status == 302

			async with session.get(url+'/save_array') as resp:
				assert resp.status == 200
	
			async with session.get(url+'/show') as resp:
				assert resp.status == 200
				assert (await resp.text()) == '"Hello"|"Redirect"|["This", "works", "too"]'

			async with session.get(url+'/show') as resp:
				assert resp.status == 200
				assert (await resp.text()) == ''

	app.loop.run_until_complete(test())
