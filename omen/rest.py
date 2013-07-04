import json
import urllib
import urllib2

class Images(object):
	def __init__(self):
		self.url = 'http://localhost:8080/images'

	def append(self, sign):
		params = encode_params(sign)
		f = urllib2.urlopen(self.url, params)
		data = f.read()
		f.close()

	def override(self, sign):
		data = json.dumps(sign)
		opener = urllib2.build_opener(urllib2.HTTPHandler)
		request = urllib2.Request(self.url, data=data)
		request.add_header('Content-Type', 'application/json')
		url = opener.open(request)

	def remove(self, sign):
		params = encode_params(sign)
		opener = urllib2.build_opener(urllib2.HTTPHandler)
		request = urllib2.Request(self.url + "?" + params)
		request.get_method = lambda: 'DELETE'
		url = opener.open(request)

def encode_params(sign):
	params = []
	for tag in sign.get('tags', []):
		params.append(('tags', tag))
	for filename in sign.get('files', []):
		params.append(('files', filename))
	return urllib.urlencode(params)
