import sys
import os.path
import sh
import yaml

def get_tag_with_parent(tag, parent):
	tags = []
	for t in tag.split(" "):
		if t.startswith("%s:" % parent) or tag.startswith("-%s:" % parent):
			tags.append(t)
		elif t.startswith("-"):
			tags.append("-%s:%s" % (parent, t[1:]))
		else:
			tags.append("%s:%s" % (parent, t))
	return [f.strip() for f in sh.tmsu("files", "--", tags)]

def get_tag(tag, parent=None):
	if parent:
		return get_tag_with_parent(tag, parent)
	tags = []
	for t in tag.split(" "):
		tags.append(t)
	return [f.strip() for f in sh.tmsu("files", "--", tags)]

def get_raw_sign(filename):
	sign = {}
	fullname = os.path.abspath(os.path.expanduser(filename))
	with file(fullname) as signfn:
		signfile = yaml.load(signfn)
		if signfile.has_key('files'):
			for f in signfile['files']:
				sign['files'] = add_file(sign.setdefault('files', []), f, os.path.dirname(fullname))
		if signfile.has_key('tags'):
			sign['tags'] = signfile['tags']
	return sign

def get_sign(filename):
	filelist = []
	fullname = os.path.abspath(os.path.expanduser(filename))
	with file(fullname) as signfn:
		signfile = yaml.load(signfn)
		if signfile.has_key('files'):
			for f in signfile['files']:
				filelist = add_file(filelist, f, os.path.dirname(fullname))
		if signfile.has_key('tags'):
			for t in signfile['tags']:
				files = get_tag(t)
				for f in files:
					filelist = add_file(filelist, f, os.path.dirname(fullname))
	return filelist

def add_file(filelist, f, signpath):
	if os.path.exists(f):
		filelist.append(os.path.abspath(f))
	elif os.path.exists(signpath + "/" + f):
		filelist.append(signpath + "/" + f)
	else:
		sys.stderr.write("Cannot find %s" % f)
	return filelist

def find_sign(dirname, sign):
	try:
		dirname = os.path.abspath(os.path.expanduser(dirname))
		while dirname != "/":
			if os.path.exists("%s/%s.sign" % (dirname, sign)):
				return "%s/%s.sign" % (dirname, sign)
			dirname = os.path.dirname(dirname)
	except Exception, e:
		return None
