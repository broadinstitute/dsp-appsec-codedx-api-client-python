import logging
from enum import Enum

import requests
from requests import Response
from requests.exceptions import ContentDecodingError, HTTPError


class BaseAPIClient(object):

	def __init__(self, base_url: str, api_key: str):
		"""Constructor for the base CodeDx API client

		Args:
			base_url (str): The CodeDx base url. Must be in the correct format: https://[CODEDX-HOST]/codedx
			api_key (str): An API key from CodeDx.
		"""
		self.base_url = base_url
		self.api_key = api_key
		self.headers = {
			'API-Key': self.api_key,
			'accept': 'application/json',
			'Content-Type': 'application/json'
		}

	def _compose_url(self, path: str):
		return self.base_url + path

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

	def get(self, path, json_data=None, content_type='application/json;charset=utf-8', local_headers=None):
		""" Composes a get request to CodeDx

		Args:
			path ([type]): [description]
			json_data ([type], optional): [description]. Defaults to None.
			content_type (str, optional): [description]. Defaults to 'application/json;charset=utf-8'.
			local_headers ([type], optional): [description]. Defaults to None.

		Returns:
			[type]: [description]
		"""
		url = self._compose_url(path)
		headers = self._compose_headers(local_headers)
		res = requests.get(url, headers=headers)
		return res

	def download(self, path, json_data=None, content_type='application/json;charset=utf-8', local_headers=None):
		url = self._compose_url(path)
		headers = self._compose_headers(local_headers)
		res = requests.get(url, headers=headers)
		return res

	def post(self, path, json_data=None, content_type='application/json;charset=utf-8', local_headers=None):
		url = self._compose_url(path)
		headers = self._compose_headers(local_headers)
		res = requests.post(url, headers=headers, json=json_data)
		return res

	def upload(self, path, file_data, local_headers=None):
		url = self._compose_url(path)
		headers = self._compose_headers(local_headers)
		headers.pop('Content-Type', None)
		with open(file_data['file_path'], 'rb') as f:
			files = {
				'file': (file_data['file_name'], f, file_data['file_type'])
			}
			res = requests.post(url, headers=headers, files=files)
		return res

	def put(self, path, json_data, content_type='application/json;charset=utf-8', local_headers=None):
		url = self._compose_url(path)
		headers = self._compose_headers(local_headers)
		res = requests.put(url,headers=headers,json=json_data)
		return res

	def delete(self, path, json_data=None, content_type='application/json;charset=utf-8', local_headers=None):
		url = self._compose_url(path)
		headers = self._compose_headers(local_headers)
		res = requests.delete(url, headers=headers)
		return res


class ContentType(str, Enum):
	"""Enumerates accepted content types"""
	JSON = 'application/json;charset=utf-8'
	CSV = 'text/csv'
	PDF = 'application/pdf'
	XML = 'text/xml'
	TEXT = 'text/plain'

	def text(self) -> str:
		""" Get status in format that will be accepted by CodeDx

		Returns:
			str: Finding status
		"""
		return str(self.value)

class ResponseHandler:
	def __init__(self, response):
		"""Initialize a Response Handler for requests.Response object"""
		self.response = response

	def validate(self):		
		"""Validate response by raising exceptions for unexpected return values"""
		if self.response.status_code > 299:
			error = f"Error from CodeDx (Status Code {self.response.status_code})"
			if self.response.content:
				error += f": { self.response.content }"
			elif self.response.text:
				error += f": { self.response.text }"
			raise HTTPError(error)

	def get_data(self):
		"""Temp"""
		self.validate()
		if self.response.json():
			return self.response.json()
		return None


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
	def __init__(self, response: Response, content: ContentType):
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
