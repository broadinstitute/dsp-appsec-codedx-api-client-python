import unittest
from unittest.mock import patch

from codedx_api.APIs import JobsAPI
from tests.MockResponses import DataMock, JSONMock

# DO NOT UPDATE - MOCK REQUESTS DO NOT REQUIRE CREDENTIALS
api_key = "0000-0000-0000-0000"
base_url = "sample-url.codedx.com"

class JobsAPI_test(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		self.job_api = JobsAPI.Jobs(api_key, base_url)


	@patch('requests.get')
	def test_job_status(self, mock_job_status):
		mock_job_status.return_value = JSONMock()
		test_job = "string"
		result = self.job_api.job_status(test_job)
		self.assertIsInstance(result, dict)

	@patch('requests.get')
	def test_job_result(self, mock_job_result):
		content_type = 'text/csv'
		test_data = "test"
		mock_job_result.return_value = DataMock(content_type, test_data)
		test_job = "string"
		result = self.job_api.job_result(test_job, 'text/csv')
		self.assertTrue(result is not None)
		self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main()
