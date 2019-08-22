import unittest
import os
from unittest.mock import MagicMock, patch
from apiclient.apiclient import APIClient, APIResponse

# DO NOT UPDATE - MOCK REQUESTS DO NOT REQUIRE CREDENTIALS
api_key = "0000-0000-0000-0000"
base_url = "https://[CODE_DX_BASE_URL].org/codedx"

class apiclient_test(unittest.TestCase):
	def setUp(self):
		unittest.TestCase.setUp(self)
		self.api_client = APIClient(base_url, api_key)

	def test__compose_url(self):
		local = "/test"
		result = self.api_client._compose_url(local)
		self.assertEqual(result, base_url + local)

	def test__compose_headers(self):
		headers = {
			'API-Key': api_key, 
			'accept': 'application/json;charset=utf-8', 
			'Content-Type': 'application/json'
		}
		new_headers = {'new_headers': 'test'}
		update_headers = {'accept': 'text/csv'}
		result = self.api_client._compose_headers({})
		self.assertTrue("API-Key" in result)
		self.assertTrue("accept" in result)
		self.assertTrue("Content-Type" in result)
		self.assertTrue(len(result) == 3)
		for key in headers.keys():
			self.assertEqual(headers[key], result[key])
		result = self.api_client._compose_headers(new_headers)
		self.assertTrue(len(result) == 4)
		self.assertTrue("new_headers" in result)
		self.assertEqual(result["new_headers"], new_headers["new_headers"])
		result = self.api_client._compose_headers(update_headers)
		self.assertTrue(len(result) == 3)
		self.assertEqual(update_headers['accept'], result['accept'])

	def test_type_check(self):
		with self.assertRaises(Exception):
			self.api_client.type_check("hello", int, "test")
		with self.assertRaises(Exception):
			self.api_client.type_check(None, str, "test")
		self.assertTrue(self.api_client.type_check("hi", str, "test"))
		self.assertTrue(self.api_client.type_check(False, bool, "test"))
		self.assertTrue(self.api_client.type_check(-3, int, "test"))

	@patch('requests.get')
	def test__get(self, mock_get):
		mock_get.return_value.json.return_value = {"test": "testing_get"}
		mock_get.return_value.status_code = 200
		mock_get.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		url = base_url + "/test"
		headers = {
			'API-Key': api_key, 
			'accept': 'application/json;charset=utf-8', 
			'Content-Type': 'application/json'
		}
		json = {"field": "test"}
		content_type = "application/json;charset=utf-8"
		result = self.api_client._get(url, headers, json, content_type)
		self.assertTrue("test" in result)
		self.assertEqual(result["test"], "testing_get")
		mock_get.return_value.content = "my test string"
		mock_get.return_value.status_code = 200
		mock_get.return_value.headers = {"Content-Type": 'text/csv'}
		url = base_url + "/test"
		headers = {
			'API-Key': api_key, 
			'accept': 'text/csv', 
			'Content-Type': 'application/json'
		}
		json = {"field": "test"}
		content_type = "text/csv"
		result = self.api_client._get(url, headers, json, content_type)
		self.assertEqual(result, "my test string")

	@patch('requests.post')
	def test__get(self, mock_post):
		mock_post.return_value.json.return_value = {"test": "testing_post"}
		mock_post.return_value.status_code = 200
		mock_post.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		url = base_url + "/test"
		headers = {
			'API-Key': api_key, 
			'accept': 'application/json;charset=utf-8', 
			'Content-Type': 'application/json'
		}
		json = {"field": "test"}
		content_type = "application/json;charset=utf-8"
		result = self.api_client._post(url, headers, json, content_type)
		self.assertTrue("test" in result)
		self.assertEqual(result["test"], "testing_post")
		mock_post.return_value.status_code = 202
		mock_post.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		mock_post.return_value.json.return_value = {"test": "testing_202"}
		result = self.api_client._post(url, headers, json, content_type)
		self.assertEqual(result["test"], "testing_202")

	@patch('builtins.open')
	@patch('requests.post')
	def test__upload(self, mock_upload, mock_open):
		mock_upload.return_value.json.return_value = {"test": "testing_upload"}
		mock_upload.return_value.status_code = 202
		mock_upload.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		mock_open.return_value.content = "this is a test string"
		url = base_url + "/test"
		headers = {
			'API-Key': api_key, 
			'accept': 'application/json;charset=utf-8', 
			'Content-Type': 'application/json'
		}
		json = {"file_name": "testdata.xml", "file_path": "./examples/testdata.xml", "file_type": "text/xml"}
		content_type = "application/json;charset=utf-8"
		result = self.api_client._upload(url, headers, json, content_type)
		self.assertEqual(result["test"], "testing_upload")
		with self.assertRaises(Exception):
			json = {"file_path": "./examples/testdata.xml", "file_type": "text/xml"}
			result = self.api_client._upload(url, headers, json, content_type)
		with self.assertRaises(Exception):
			json = {"file_name": "testdata.xml", "file_type": "text/xml"}
			result = self.api_client._upload(url, headers, json, content_type)
		with self.assertRaises(Exception):
			json = {"file_name": "testdata.xml", "file_path": "./examples/testdata.xml"}
			result = self.api_client._upload(url, headers, json, content_type)
		json = {"X-Client-Request-Id": "random", "file_name": "testdata.xml", "file_path": "./examples/testdata.xml", "file_type": "text/xml"}
		result = self.api_client._upload(url, headers, json, content_type)
		self.assertEqual(result["test"], "testing_upload")

	@patch('requests.put')
	def test__put(self, mock_put):
		mock_put.return_value.status_code = 201
		mock_put.return_value.headers = {"Content-Type": None}
		url = base_url + "/test"
		headers = {
			'API-Key': api_key, 
			'accept': 'application/json;charset=utf-8', 
			'Content-Type': 'application/json'
		}
		json = {"test": "testing"}
		content_type = None
		result = self.api_client._put(url, headers, json, content_type)
		self.assertTrue("status"in result)
		self.assertEqual(result["status"], "Success")

	@patch('requests.delete')
	def test__delete(self, mock_delete):
		mock_delete.return_value.status_code = 204
		mock_delete.return_value.headers = {"Content-Type": None}
		url = base_url + "/test"
		headers = {
			'API-Key': api_key, 
			'accept': 'application/json;charset=utf-8', 
			'Content-Type': 'application/json'
		}
		json = {"test": "testing"}
		content_type = None
		result = self.api_client._delete(url, headers, json, content_type)
		self.assertTrue("status"in result)
		self.assertEqual(result["status"], "Success")

	@patch('requests.post')
	@patch('requests.get')
	def test_call(self, mock_get, mock_post):
		mock_get.return_value.json.return_value = {"test": "testing_get"}
		mock_get.return_value.status_code = 200
		mock_get.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		url = base_url + "/test"
		json = {"field": "test"}
		content_type = "application/json;charset=utf-8"
		result = self.api_client.call("GET", url, json, content_type, {'test': 'new_header'})
		self.assertTrue("test" in result)
		self.assertEqual(result["test"], "testing_get")
		result = self.api_client.call("GET", url)
		self.assertTrue("test" in result)
		mock_post.return_value.json.return_value = {"test": "testing_get"}
		mock_post.return_value.status_code = 200
		mock_post.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		url = base_url + "/test"
		json = {"field": "test"}
		content_type = "application/json;charset=utf-8"
		result = self.api_client.call("POST", url, json, content_type, {'test': 'new_header'})
		self.assertTrue("test" in result)
		self.assertEqual(result["test"], "testing_get")

	def test_validate(self):
		mock_get = MagicMock()
		mock_get.json.return_value = {"test": "testing_get"}
		mock_get.status_code = 200
		mock_get.headers = {"Content-Type": 'application/json;charset=utf-8'}
		resp = APIResponse(mock_get, 'application/json;charset=utf-8')
		with self.assertRaises(Exception):
			resp = APIResponse(mock_get, 'text/csv')
		with self.assertRaises(Exception):
			mock_get.status_code = 500
			resp = APIResponse(mock_get, 'application/json;charset=utf-8')

	def test_get_data(self):
		mock_get = MagicMock()
		mock_get.json.return_value = {"test": "testing_get_data"}
		mock_get.status_code = 200
		mock_get.headers = {"Content-Type": 'application/json;charset=utf-8'}
		resp = APIResponse(mock_get, 'application/json;charset=utf-8')
		result = resp.getData()
		self.assertTrue(result["test"], "testing_get_data")

if __name__ == '__main__':
    unittest.main()
