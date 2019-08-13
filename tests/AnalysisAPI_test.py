import unittest
import os
from unittest.mock import MagicMock, patch
from apiclient.APIs import AnalysisAPI

# DO NOT UPDATE - MOCK REQUESTS DO NOT REQUIRE CREDENTIALS
api_key = "0000-0000-0000-0000"
base_url = "sample-url.codedx.com"

class AnalysisAPI_test(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		self.analysis_api = AnalysisAPI.Analysis(api_key, base_url)
		self.mprojs = {
			  "projects": [
			    {
			      "id": 1,
			      "name": "MockProj"
			    },
			    {
			      "id": 2,
			      "name": "ProjMock"
			    }
			  ]
			}
		self.manalysis = {
							"prepId": "string",
							"verificationErrors": [
								"string"
							],
							"scmSetup": {
								"scmInfo": {
									"repoType": "string",
									"url": "string",
									"rev": {
										"revType": "branch",
										"revName": "string",
										"revDetail": "string"
									}
								},
								"inputId": "myInputId",
								"setupJobId": "string"
							}
						}

	@patch('requests.get')
	@patch('requests.post')
	def test_create_analysis(self, mock_create_analysis, mock_projects):
		mock_create_analysis.return_value.json.return_value = self.manalysis
		mock_create_analysis.return_value.status_code = 200
		mock_create_analysis.return_value.headers= {"Content-Type": 'application/json;charset=utf-8'}
		mock_projects.return_value.json.return_value = self.mprojs
		mock_projects.return_value.status_code = 200
		mock_projects.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		test_proj = self.mprojs['projects'][0]['name']
		result = self.analysis_api.create_analysis(test_proj)
		self.assertTrue('prepId' in result)
		self.assertTrue(isinstance(result['prepId'], str))
		self.assertEqual(self.manalysis["scmSetup"]["inputId"], result["scmSetup"]["inputId"])
		with self.assertRaises(Exception):
			self.analysis_api.create_analysis(-1)

	@patch('requests.get')
	def test_get_prep(self, mock_get_prep):
		mock_get_prep.return_value.json.return_value = {
															"inputIds": [
																"myInputId"
															],
															"verificationErrors": [
																"string"
															]
														}
		mock_get_prep.return_value.status_code = 200
		mock_get_prep.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.analysis_api.get_prep(self.manalysis["prepId"])
		self.assertTrue(isinstance(result["inputIds"], list))

	@patch('requests.post')
	def test_upload_analysis(self, mock_upload_analysis):
		mock_upload_analysis.return_value.json.return_value = {
																"jobId": "myJobString",
																"inputId": "string",
																"size": 0
															}
		mock_upload_analysis.return_value.status_code = 202
		mock_upload_analysis.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		test_prep_id = "myTestPrep"
		test_file_name = os.path.join(os.path.dirname(__file__), 'testdata.xml')
		result = self.analysis_api.upload_analysis(test_prep_id, test_file_name)
		self.assertEqual(result["jobId"], "myJobString")
		with self.assertRaises(Exception):
			self.analysis_api.upload_analysis(-5, test_file_name)
		with self.assertRaises(Exception):
			self.analysis_api.upload_analysis(test_prep_id, "Not a valid file name")
		with self.assertRaises(Exception):
			self.analysis_api.upload_analysis(test_prep_id, "not_valid_ext.html")

	@patch('requests.post')
	def test_run_analysis(self, mock_run_analysis):
		mock_run_analysis.return_value.json.return_value = {
															"analysisId": 0,
															"jobId": "runningAnalysis"
														}
		mock_run_analysis.return_value.status_code = 202
		mock_run_analysis.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		test_prep_id = "myTestPrep"
		result = self.analysis_api.run_analysis(test_prep_id)
		self.assertEqual(result["jobId"], "runningAnalysis")
		self.assertEqual(result["analysisId"], 0)
		with self.assertRaises(Exception):
			self.analysis_api.run_analysis(-5)

	@patch('requests.get')
	def test_get_analysis(self, mock_get_analysis):
		mock_get_analysis.return_value.json.return_value = {
																"id": 0,
																"projectId": 3,
																"state": "string",
																"createdBy": {
																	"id": 0,
																	"name": "string"
																},
																"creationTime": "string",
																"startTime": "string",
																"endTime": "string",
																"name": "string"
															}
		mock_get_analysis.return_value.status_code = 200
		mock_get_analysis.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		self.analysis_api.projects_api.projects = {'MockProj': 3}
		result = self.analysis_api.get_analysis('MockProj', 0)
		self.assertEqual(result["id"], 0)
		self.assertEqual(result["projectId"], 3)

if __name__ == '__main__':
    unittest.main()

