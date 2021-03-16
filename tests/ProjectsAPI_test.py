import unittest
from unittest.mock import patch

from codedx_api.APIs import ProjectsAPI
from MockResponses import JSONMock, SuccessMock

# DO NOT UPDATE - MOCK REQUESTS DO NOT REQUIRE CREDENTIALS
api_key = "0000-0000-0000-0000"
base_url = "sample-url.codedx.com"

class ProjectsAPI_test(unittest.TestCase):


	def setUp(self):
		unittest.TestCase.setUp(self)
		self.proj_api = ProjectsAPI.Projects(api_key, base_url)


	@patch('requests.get')
	def test_get_projects(self, mock_get_projects):
		# Creating Mock
		mock_get_projects.return_value = JSONMock()
		projs = self.proj_api.get_projects()
		self.assertIsInstance(projs, dict)


	@patch('requests.put')
	def test_create_project(self, mock_create_project):
		mock_create_project.return_value = JSONMock()
		test_name = "CreateTest"
		result = self.proj_api.create_project(test_name)
		self.assertIsInstance(result, dict)


	@patch('requests.put')
	def test_update_project(self, mock_update_project):
		mock_update_project.return_value = SuccessMock()
		test_name = "UpdateTest"
		test_id = 1
		result = self.proj_api.update_project(test_id, new_name=test_name)


	@patch('requests.delete')
	def test_delete_project(self, mock_delete_project):
		mock_delete_project.return_value.status_code = 204
		test_id = 1
		result = self.proj_api.delete_project(test_id)


	@patch('requests.post')
	def test_query_project(self, mock_query_projects):
		mock_query_projects.return_value = JSONMock()
		mock_query_projects.return_value.data = [{"project": "test"}, {"project2": "test"}]
		filters = {
			"name": "WebGoat",
			"metadata": {
				"Project Owner": "Jim",
				"id:5": "Medium",
				"My Tag Field": "hello goodbye "
			}
		}
		result = self.proj_api.query_projects(filters)
		self.assertIsInstance(result, list)
		result = self.proj_api.query_projects(filters, 5, 2)
		self.assertIsInstance(result, list)


	@patch('requests.post')
	def test_query_count(self, mock_query_count):
		mock_query_count.return_value = JSONMock()
		mock_query_count.return_value.data = 5
		filters = {
			"name": "WebGoat"
		}
		result = self.proj_api.query_count(filters)
		self.assertIsInstance(result, int)


	@patch('requests.get')
	def test_project_status(self, mock_project_status):
		mock_project_status.return_value = JSONMock()
		result = self.proj_api.project_status(0)
		self.assertIsInstance(result, dict)


	@patch('requests.post')
	def test_file_mappings(self, mock_file_mappings):
		mock_file_mappings.return_value = JSONMock()
		result = self.proj_api.file_mappings(0, {"files": "/Proj/foo"})
		self.assertIsInstance(result, dict)


	@patch('requests.get')
	def test_project_files(self, mock_project_files):
		mock_project_files.return_value = JSONMock()
		mock_project_files.return_value.data = ["file1", "file2"]
		result = self.proj_api.project_files(0)
		self.assertIsInstance(result, list)


	@patch('requests.get')
	def test_project_roles(self, mock_project_roles):
		mock_project_roles.return_value = JSONMock()
		mock_project_roles.return_value.data = ["Admin", "Creator"]
		result = self.proj_api.project_roles(0)


	@patch('requests.get')
	def test_project_user(self, mock_project_user):
		mock_project_user.return_value = JSONMock()
		result = self.proj_api.project_user(0, 0)
		self.assertIsInstance(result, dict)


	@patch('requests.put')
	def test_project_user(self, mock_update_user):
		mock_update_user.return_value = SuccessMock()
		roles = {
			"Reader": True,
			"Updater": True,
			"Creator": True,
			"Manager": True
		}
		result = self.proj_api.update_user_role(0, 0, roles)
		self.assertIsNone(result)


	@patch('requests.post')
	def test_get_project_id(self, mock_get_id):
		mock_get_id.return_value = JSONMock()
		mock_result = [
			{
				"id": 0,
				"name": "Webgoat"
			}
		]
		mock_get_id.return_value.data = mock_result
		result = self.proj_api.get_project_id("Webgoat")
		self.assertEqual(result, mock_result[0]["id"])


if __name__ == '__main__':
    unittest.main()
