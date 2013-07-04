#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
	name="omen",
	version="0.1.1",
	url = "https://github.com/devonjones/omen",
	author="Devon Jones",
	author_email="devon.jones@gmail.com",
	license = "Apache",
	scripts = [
		"bin/omen-swap-playlist",
		"bin/omen-swap-pictures",
		"bin/omen-service",
		"bin/omen"],
	packages=find_packages(),
	install_requires=[
		"sh",
		"python-mpd",
		"pyyaml",
		"k.config",
		"tornado"
	],
	package_data = {
		"static": ["*.html", "*.css", "*.js"]
	},
	description = "Omen RPG technology conductor",
)
