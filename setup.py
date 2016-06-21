# coding=utf-8
from distutils.core import setup
from setuptools import setup, find_packages

"""
Session flash messages for aiohttp.web
"""

setup(
	name='aiohttp_session_flash',
	version='0.0.1',
	url='https://github.com/IlyaSemenov/aiohttp_session_flash',
	license='BSD',
	author='Ilya Semenov',
	author_email='ilya@semenov.co',
	description=__doc__,
	long_description=open('README.rst').read(),
	packages=['aiohttp_session_flash'],
	install_requires=['aiohttp>=0.21.6', 'aiohttp_session>=0.5.0'],
	classifiers=[],
)
