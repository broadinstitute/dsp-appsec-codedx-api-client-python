import logging
from enum import Enum

import requests
from requests import Response
from requests.exceptions import ContentDecodingError


class BaseAPIClient(object):

	def __init__(self, base, api_key, verbose = False):
		"""Base API Client for requests."""
		self.verbose = verbose
		self.base_path = base
		self.api_key = api_key
		self.headers = {
			'API-Key': self.api_key,
			'accept': 'application/json',
			'Content-Type': 'application/json'
		}
		self.commands = {
			"GET": self._get,
			"POST": self._post,
			"PUT": self._put,
			"DELETE": self._delete,
			"UPLOAD": self._upload,
			"DOWNLOAD": self._download
		}

	def _compose_url(self,local_path):
		return self.base_path + local_path

	def _compose_headers(self,local_headers):
		headers = self.headers
		if local_headers == None:
			local_headers = {}
		for key in local_headers:
			headers[key] = local_headers[key]
		return headers

	@staticmethod
	def type_check(inp, t, field):
		if not isinstance(inp, t):
			msg = "%s is not of type %s" % (field, t)
			raise Exception(msg)
		return True

	@staticmethod
	def _get(url, headers, json_data, content_type):
		res = JSONResponseHandler(requests.get(url, headers=headers))
		return res.get_data()

	@staticmethod
	def _download(url, headers, json_data, content_type):
		res = ContentResponseHandler(requests.get(url, headers=headers), content_type)
		return res.get_data()

	@staticmethod
	def _post(url, headers, json_data, content_type):
		res = JSONResponseHandler(requests.post(url, headers=headers, json=json_data))
		return res.get_data()

	def _upload(self, url, headers, json_data, content_type):
		if 'file_name' not in json_data or 'file_path' not in json_data or 'file_type' not in json_data:
			raise Exception("Missing file data.")
		headers = {'API-Key': self.api_key, 
			'accept': 'application/json'}
		if 'X-Client-Request-Id' in json_data:
			headers['X-Client-Request-Id'] = json_data['X-Client-Request-Id']
		f = open(json_data['file_path'], 'rb')
		files = {
			'file': (json_data['file_name'], f, json_data['file_type'])
		}
		res = JSONResponseHandler(requests.post(url, headers=headers, files=files))
		f.close()
		return res.get_data()

	@staticmethod
	def _put(url, headers, json_data, content_type):
		res = ResponseHandler(requests.put(url,headers=headers,json=json_data))
		return res.get_data()

	@staticmethod
	def _delete(url, headers, json_data, content_type):
		res = ResponseHandler(requests.delete(url, headers=headers))
		return res.get_data()

	def call(self, method, local_path, json_data=None, content_type='application/json;charset=utf-8', local_headers=None):
		url = self._compose_url(local_path)
		headers = self._compose_headers(local_headers)
		return self.commands[method](url, headers, json_data, content_type)

class ContentType(str, Enum):
    """Enumerates accepted content types"""

    JSON = 'application/json;charset=utf-8'
    CSV = 'text/csv'
    PDF = 'application/pdf'
    XML = 'text/xml'


class ResponseHandler:
	def __init__(self, response):
		"""Initialize a Response Handler for requests.Response object"""
		self.response = response

	def validate(self):		
		"""Validate response by raising exceptions for unexpected return values"""
		if self.response.status_code > 299:
			self.response.raise_for_status()

	def get_data(self):
		"""Temp"""
		self.validate()
		if self.response.json():
			return self.response.json()
		return { 'status': 'Success'}


class JSONResponseHandler(ResponseHandler):
	def validate(self):
		"""Validate response by raising exceptions for unexpected return values"""
		super().validate()
		if ("Content-Type" not in self.response.headers or 
			self.response.headers["Content-Type"] != ContentType.JSON):
			raise ContentDecodingError("Error: CodeDx Response was not type JSON.")

	def get_data(self) -> dict:
		"""Returns a JSON dictionary with response data"""
		self.validate()
		return self.response.json()


class ContentResponseHandler(ResponseHandler):
	def __init__(self, response, content):
		"""Initialize Content Response Handler"""
		self.response = response
		self.content = content

	def validate(self):
		"""Validate Response by raising exceptions for unexpected return values"""
		super().validate()
		if ("Content-Type" not in self.response.headers or 
			self.response.headers["Content-Type"] != self.content):
			raise ContentDecodingError("Error: CodeDx Response does not match accepted type.")

	def get_data(self):
		"""Returns the content of the response"""
		self.validate()
		return self.response.content
