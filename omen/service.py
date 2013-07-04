import json
import tornado.web
import logging
from omen.cache import TagCache, ImageListCache, file_validaton_closure
from tornado.options import options

class TagListHandler(tornado.web.RequestHandler):
	def get(self):
		if TagCache().cache == None:
			TagCache().refresh_cache()
		self.set_header('Content-Type', "application/json")
		self.write(json.dumps(TagCache().cache, indent=2))
		self.write("\n")

class ImageListHandler(tornado.web.RequestHandler):
	def prepare(self):
		if self.request.headers.get("Content-Type") == "application/json":
			self.json_args = json.loads(self.request.body)
		else:
			self.json_args = None

	def get(self):
		self.set_header('Content-Type', "application/json")
		self.write(json.dumps(ImageListCache().cache, indent=2))
		self.write("\n")

	def post(self):
		validator = file_validaton_closure(options.content)
		if self.json_args:
			# Overwrite
			ImageListCache.clear()
			for tag in self.json_args.get('tags', []):
				ImageListCache.add_tag(tag, validator)
			for fn in self.json_args.get('files', []):
				ImageListCache.add_file(fn, validator)
		else:
			for tag in self.get_arguments('tags'):
				ImageListCache.add_tag(tag, validator)
			for fn in self.get_arguments('files'):
				ImageListCache.add_file(fn, validator)
		self.set_header('Content-Type', "application/json")
		self.write(json.dumps(ImageListCache().cache, indent=2))
		self.write("\n")

	def delete(self):
		validator = file_validaton_closure(options.content)
		for tag in self.get_arguments('tags'):
			ImageListCache.remove_tag(tag, validator)
		for fn in self.get_arguments('files'):
			ImageListCache.remove_file(fn, validator)
		self.set_header('Content-Type', "application/json")
		self.write(json.dumps(ImageListCache().cache, indent=2))
		self.write("\n")

class ImageHandler(tornado.web.RequestHandler):
	def get(self):
		fn = ImageListCache().rotate()
		if fn:
			content = {"image": fn}
			self.set_header('Content-Type', "application/json")
			self.write(json.dumps(content, indent=2))
			self.write("\n")
		else:
			self.set_status(201)
#	def post(self, instance_id):
#		subdomain = self.get_argument('subdomain')
#		creds, domain_name = AWSCreds.get_name_for_headers(self.request.headers)
#		sdbconn = k.aws.sdb.connect(creds)
#		r53conn = k.aws.route53.connect(creds)
#		domain = sdbconn.get_domain(domain_name)
#		try:
#			record = apply_instance_name(creds, r53conn, domain, instance_id, subdomain)
#			self.set_header('Content-Type', "application/json")
#			self.write(json.dumps(record, indent=2))
#			self.write("\n")
#		except ExistsException, ee:
#			self.set_status(500)
#			self.write(str(ee))
#		except Exception, e:
#			self.set_status(500)
#			self.write("Unexpected error:", sys.exc_info()[0])
#		finally:
#			sdbconn.close()
#			r53conn.close()


