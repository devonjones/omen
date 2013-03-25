#!/usr/bin/env python
import sys
import time
import os
import os.path
import sh
import mpd
import random
from optparse import OptionParser

def get_tag(tag, strip):
	tags = []
	for t in tag.split(" "):
		if t.startswith("music:") or tag.startswith("-music:"):
			tags.append(t)
		elif t.startswith("-"):
			tags.append("-music:%s" % t[1:])
		else:
			tags.append("music:%s" % t)
	files = sh.tmsu("files", "--", tags)
	return [f.replace(strip, '').strip() for f in files]

def play_tag(client, tags, strip):
	files = set()
	for tag in tags:
		files.update(get_tag(tag, strip))
	files = list(files)
	random.shuffle(files)
	curr = client.currentsong()
	if curr and curr['file'] in files:
		rotate(client, curr, files)
	else:
		replace(client, files)

def remove_list(client, curr_id):
	for song in client.playlistinfo():
		if song['id'] != curr_id:
			client.deleteid(song['id'])

def rotate(client, curr, files):
	client.random(1)
	remove_list(client, curr['id'])
	for f in files:
		client.add(f)

def replace(client, files):
	vol = int(client.status()['volume'])
	if vol >= 0:
		fade(client, vol)
	client.clear()
	for f in files:
		client.add(f)
	if vol >= 0:
		client.setvol(vol)
	client.play()

def fade(client, vol):
	while vol > 0:
		vol = vol - 1
		client.setvol(vol)
		time.sleep(.2)

def main():
	usage =  "usage: %prog [options]\n\n"
	usage += "Plays music based on tmsu tag via mpd."
	parser = option_parser(usage)
	(options, args) = parser.parse_args()
	if not options.tags or len(options.tags) == 0:
		sys.stderr.write("-t must be used one or more times\n")
		sys.exit(1)
	client = mpd.MPDClient()
	client.connect(options.host, options.port)
	play_tag(client, options.tags, options.strip)

def option_parser(usage):
	parser = OptionParser(usage=usage)
	parser.add_option("-H", "--host", dest="host", default="localhost",
		help="MPD host (default: localhost)")
	parser.add_option("-p", "--port", dest="port", default=6600, type="int",
		help="MPD port (default: 6600)")
	parser.add_option("-t", "--tags", dest="tags", action="append",
		help="tags: can use -t multiple times if you want more then one tag collection")
	parser.add_option("-s", "--strip", dest="strip",
		help="prefix to strip from file names before sending them to mpd")
	return parser

if __name__ == "__main__":
	sys.exit(main())

