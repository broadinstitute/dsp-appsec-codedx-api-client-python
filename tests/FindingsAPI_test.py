import unittest
from unittest.mock import patch

from codedx_api.APIs.BaseAPIClient import ContentType
from codedx_api.APIs.FindingsAPI import Findings
from MockResponses import DataMock, JSONMock

# DO NOT UPDATE - MOCK REQUESTS DO NOT REQUIRE CREDENTIALS
api_key = "0000-0000-0000-0000"
base_url = "sample-url.codedx.com"

class FindingsAPI_test(unittest.TestCase):


	def setUp(self):
		unittest.TestCase.setUp(self)
		self.findings_api = Findings(api_key, base_url)
		self.test_project = 0
		self.request_filters = {"sort": {"by": "id", "direction": "ascending"}}


	@patch('requests.get')
	def test_get_finding(self, mock_get_finding):
		mock_get_finding.return_value = JSONMock()
		result = self.findings_api.get_finding(5)
		self.assertIsInstance(result, dict)
		result = self.findings_api.get_finding(5, ["triage-time"])
		self.assertIsInstance(result, dict)


	@patch('requests.get')
	def test_get_finding_description(self, mock_get_finding_description):
		mock_get_finding_description.return_value = JSONMock()
		result = self.findings_api.get_finding_description(5)
		self.assertIsInstance(result, dict)


	@patch('requests.get')
	def test_get_finding_history(self, mock_get_finding_history):
		mock_get_finding_history.return_value = JSONMock()
		mock_get_finding_history.return_value.data = ["findings"]
		result = self.findings_api.get_finding_history(5)
		self.assertIsInstance(result, list)


	@patch('requests.post')
	def test_get_finding_table(self, mock_get_finding_table):
		mock_get_finding_table.return_value = JSONMock()
		mock_get_finding_table.return_value.data = ["findings"]
		result = self.findings_api.get_finding_table(self.test_project)
		self.assertIsInstance(result, list)
		result = self.findings_api.get_finding_table(self.test_project, ['description'])
		self.assertIsInstance(result, list)
		result = self.findings_api.get_finding_table(project=self.test_project, req_body=self.request_filters)
		self.assertIsInstance(result, list)
		result = self.findings_api.get_finding_table(project=self.test_project, options=["issue"], req_body=self.request_filters)
		self.assertIsInstance(result, list)


	@patch('requests.post')
	def test_get_finding_count(self, mock_get_finding_count):
		mock_get_finding_count.return_value = JSONMock()
		result = self.findings_api.get_finding_count(self.test_project)
		self.assertIsInstance(result, dict)
		result = self.findings_api.get_finding_count(project=self.test_project, req_body=self.request_filters)
		self.assertIsInstance(result, dict)


	@patch('requests.post')
	def test_get_finding_group_count(self, mock_get_finding_group_count):
		mock_get_finding_group_count.return_value = JSONMock()
		mock_get_finding_group_count.return_value.data = [{"test": "data"}]
		filters = {
			"filter": {
				"detectionMethod": 1,
				"severity": "Medium"
			}
		}
		result = self.findings_api.get_finding_group_count(self.test_project, filters)
		self.assertIsInstance(result, list)


	@patch('requests.post')
	def test_get_finding_flow(self, mock_get_finding_flow):
		mock_get_finding_flow.return_value = JSONMock()
		mock_get_finding_flow.return_value.data = [{"findings": "test"}]
		filters = {
			"filter": {
				"detectionMethod": 1,
				"severity": "Medium"
			}
		}
		result = self.findings_api.get_finding_flow(self.test_project, filters)
		self.assertIsInstance(result, list)
		with self.assertRaises(Exception):
			self.findings_api.get_finding_flow(self.test_project)


	@patch('requests.get')
	def test_get_finding_file(self, mock_get_finding_file):
		mock_get_finding_file.return_value = DataMock(ContentType.TEXT, "text")
		result = self.findings_api.get_finding_file(self.test_project, "file")
		self.assertIsInstance(result, str)
		result = self.findings_api.get_finding_file(self.test_project, 1)
		self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
