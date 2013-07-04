import os.path
import sh

class TagCacheSingleton(object):
	def __init__(self):
		self.cache = None

	def __call__(self):
		return self

	def refresh_cache(self):
		self.cache = []
		for tag in sh.tmsu("tags", "--all"):
			tag = tag.strip()
			if tag.find(":") > -1:
				subtags = tag.split(":")
				create_tag(self.cache, subtags)
			else:
				create_tag(self.cache, [tag])

TagCache = TagCacheSingleton()

def create_tag(level, subtags):
	newsubtags = list(subtags)
	name = newsubtags.pop(0)
	existing = find(level, name)
	if not existing:
		existing = {"name": name}
		level.append(existing)
	if len(newsubtags):
		newlevel = existing.setdefault('tags', [])
		create_tag(newlevel, newsubtags)

def find(level, name):
	for item in level:
		if item.get('name') == name:
			return item

class ImageListCacheSingleton(object):
	def __init__(self):
		self.cache = []
		self.tags = set()

	def __call__(self):
		return self

	def clear(self):
		self.cache = []
		self.tags = set()

	def add_file(self, filename, validator):
		vfn = validator(filename)
		if vfn:
			if vfn not in self.cache:
				self.cache.append(vfn)
		else:
			raise Exception("File does not exist: %s" % filename)

	def add_tag(self, tag, validator):
		files = [f.strip() for f in sh.tmsu("files", "--", tag)]
		for fn in files:
			self.add_file(fn, validator)
		self.tags.add(tag)

	def refresh_tags(self, validator):
		for tag in tags:
			self.add_tag(tag)

	def remove_file(self, filename, validator):
		# Function is idempotent, will not error for removing a file
		# that has already been removed
		vfn = validator(filename)
		if vfn:
			try:
				self.cache.remove(vfn)
			except:
				pass

	def remove_tag(self, tag, validator):
		# Function is idempotent, will not error for removing a tag or files
		# that have already been removed
		files = [f.strip() for f in sh.tmsu("files", "--", tag)]
		for fn in files:
			self.remove_file(fn, validator)
		try:
			tags.remove(tag)
		except:
			pass

	def rotate(self):
		if len(self.cache):
			fn = self.cache.pop(0)
			self.cache.append(fn)
			return fn

def file_validaton_closure(root):
	def closure(filename):
		if filename.startswith(root):
			filename = filename.replace(root, '')
		testname = os.path.abspath(os.path.expanduser(root + "/" + filename))
		if os.path.isfile(testname):
			return filename
	return closure

ImageListCache = ImageListCacheSingleton()
