import os
import unittest
from unittest.mock import patch

from codedx_api.APIs.AnalysisAPI import Analysis
from tests.MockResponses import JSONMock, SuccessMock

# DO NOT UPDATE - MOCK REQUESTS DO NOT REQUIRE CREDENTIALS
api_key = "0000-0000-0000-0000"
base_url = "https://[CODE_DX_BASE_URL].org/codedx"

class AnalysisAPI_test(unittest.TestCase):


	def setUp(self):
		unittest.TestCase.setUp(self)
		self.analysis_api = Analysis(api_key, base_url)
		self.test_project = 0
		self.prep_id = "test_prep_id"


	@patch('requests.post')
	def test_create_analysis(self, mock_create_analysis):
		mock_create_analysis.return_value = JSONMock()
		result = self.analysis_api.create_analysis(self.test_project)
		self.assertIsInstance(result, dict)


	@patch('requests.get')
	def test_get_prep(self, mock_get_prep):
		mock_get_prep.return_value = JSONMock()
		result = self.analysis_api.get_prep(self.prep_id)


	@patch('requests.post')
	def test_upload_analysis(self, mock_upload_analysis):
		mock_upload_analysis.return_value = JSONMock()
		mock_upload_analysis.return_value.status_code = 202
		test_prep_id = "myTestPrep"
		test_file_name = os.path.join(os.path.dirname(__file__), 'testdata.xml')
		result = self.analysis_api.upload_analysis(self.prep_id, test_file_name)
		with self.assertRaises(Exception):
			self.analysis_api.upload_analysis(self.prep_id, "Not a valid file name")
		with self.assertRaises(Exception):
			self.analysis_api.upload_analysis(self.prep_id, "not_valid_ext.html")


	@patch('requests.post')
	def test_run_analysis(self, mock_run_analysis):
		mock_run_analysis.return_value = JSONMock()
		mock_run_analysis.return_value.status_code = 202
		result = self.analysis_api.run_analysis(self.prep_id)
		self.assertIsInstance(result, dict)


	@patch('requests.get')
	def test_get_input_metadata(self, mock_get_input_metadata):
		mock_get_input_metadata.return_value = JSONMock()
		result = self.analysis_api.get_input_metadata('1234', 'TEST')
		self.assertIsInstance(result, dict)


	@patch('requests.delete')
	def test_delete_input(self, mock_delete_input):
		mock_delete_input.return_value = SuccessMock()
		result = self.analysis_api.delete_input('1234', 'TEST')
		self.assertIsNone(result)


	@patch('requests.delete')
	def test_delete_pending(self, mock_delete_pending):
		mock_delete_pending.return_value = SuccessMock()
		result = self.analysis_api.delete_pending('1234', 'TEST')
		self.assertIsNone(result)


	@patch('requests.put')
	def test_toggle_display_tag(self, mock_toggle_display_tag):
		mock_toggle_display_tag.return_value = JSONMock()
		result = self.analysis_api.toggle_display_tag('1234', 'inputId', 'tagID', True)
		self.assertIsInstance(result, dict)


	@patch('requests.put')
	def test_enable_display_tag(self, mock_enable_display_tag):
		mock_enable_display_tag.return_value = JSONMock()
		result = self.analysis_api.enable_display_tag('1234', 'inputId', 'tagID')
		self.assertIsInstance(result, dict)


	@patch('requests.put')
	def test_disable_display_tag(self, mock_disable_display_tag):
		mock_disable_display_tag.return_value = JSONMock()
		result = self.analysis_api.disable_display_tag('1234', 'inputId', 'tagID')
		self.assertIsInstance(result, dict)


	@patch('requests.get')
	def test_get_all_analysis(self, mock_get_all_analysis):
		mock_get_all_analysis.return_value = JSONMock()
		result = self.analysis_api.get_all_analysis(self.test_project)
		self.assertIsInstance(result, dict)


	@patch('requests.get')
	def test_get_analysis(self, mock_get_analysis):
		mock_get_analysis.return_value = JSONMock()
		result = self.analysis_api.get_analysis(self.test_project, 0)
		self.assertIsInstance(result, dict)


	@patch('requests.put')
	def test_name_analysis(self, mock_name_analysis):
		mock_name_analysis.return_value = SuccessMock()
		mock_name_analysis.return_value.status_code = 204
		result = self.analysis_api.name_analysis(self.test_project, 1, 'NewName')


if __name__ == '__main__':
    unittest.main()
