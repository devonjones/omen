#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
	name="omen",
	version="0.1.1",
	url = "https://github.com/devonjones/omen",
	author="Devon Jones",
	author_email="devon.jones@gmail.com",
	license = "Apache",
	scripts = ["bin/omen-swap-playlist"],
	packages=find_packages(),
	install_requires=["sh", "python-mpd", "pyyaml", "knewton.config"],
	description = "Omen RPG technology conductory",
)
