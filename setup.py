"""Session flash messages for aiohttp.web"""
from setuptools import setup, find_packages


setup(
	name='aiohttp_session_flash',
	version='0.0.2',
	url='https://github.com/IlyaSemenov/aiohttp_session_flash',
	license='BSD',
	author='Ilya Semenov',
	author_email='ilya@semenov.co',
	description=__doc__,
	long_description=open('README.rst').read(),
	packages=['aiohttp_session_flash'],
	install_requires=['aiohttp>=0.21.6,<0.22', 'aiohttp_session>=0.5,<0.6'],
	classifiers=[],
)
