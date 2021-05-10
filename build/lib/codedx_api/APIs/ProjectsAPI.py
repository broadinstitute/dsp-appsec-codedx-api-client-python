import re

from codedx_api.APIs.BaseAPIClient import (BaseAPIClient, JSONResponseHandler,
                                           ResponseHandler)


# Projects Client for Code DX Projects API
class Projects(BaseAPIClient):
	def __init__(self, base_url: str, api_key: str):
		"""Definitions for Projects API on CodeDx

		Args:
			base (str): The CodeDx base URL. https://[CODEDX_INSTANCE]/codedx
			api_key (str): CodeDx API key
		"""
		super().__init__(base_url, api_key)
		#TODO: don't have projects stored locally
		self.projects = {}


	def __query_criteria(self, filters: dict, limit: int = None, offset: int = None) -> dict:
		"""Returns JSON body for a request to Project query endpoint

		Args:
			filters (dict): Filters for the query results
			limit (int, optional): Limits the number of results to return. Defaults to None.
			offset (int, optional): Offset for the results. Specifying an offset without a limit is an error. Defaults to None.

		Returns:
			dict: [description]
		"""
		criteria = {
			"filter": filters
		}
		if offset:
			criteria['offset'] = offset
		if limit:
			criteria['limit'] = limit
		return criteria


	def get_projects(self) -> dict:
		"""Returns the projects in a CodeDx instance

		Returns:
			dict: Returns a dictionary with a list of project names and ids
		"""
		path = '/api/projects'
		data = JSONResponseHandler(self.get(path)).get_data()
		return data


	def create_project(self, name: str) -> dict:
		"""Create a new project

		Args:
			name (str): Project name

		Returns:
			dict: Project object
		"""
		path = '/api/projects'
		params = {
			"name": name
		}
		data = JSONResponseHandler(self.put(path, params)).get_data()
		return data


	def update_project(self, project: int, new_name: str = None, parent_id: int = None) -> None:
		"""Update a project by changing its name or parent

		Args:
			project (int): Project id
			new_name (str, optional): New name for the project. Defaults to None.
			parentId (int, optional): New parent ID for the project. Defaults to None.
		"""
		path = f'/api/projects/{ project }'
		params = {}
		if parent_id:
			params['parentId'] = parent_id
		if new_name:
			params['name'] = new_name
		ResponseHandler(self.put(path, json_data=params)).validate()
		return


	def delete_project(self, project: int) -> None:
		"""Delete a project

		Args:
			project (int): Project id
		"""
		path = f'/api/projects/{ project }'
		ResponseHandler(self.delete(path)).validate()
		return


	def query_projects(self, filters: dict, limit: int = None, offset: int = None) -> list:
		"""Returns the results of a query as a list of project dictionaries

		Args:
			filters (dict): Filters for the query results
			limit (int, optional): Limits the number of results to return. Defaults to None.
			offset (int, optional): Offset for the results. Specifying an offset without a limit is an error. Defaults to None.

		Returns:
			list: List of projects
		"""
		path = '/api/projects/query'
		criteria = self.__query_criteria(filters, offset, limit)
		data = JSONResponseHandler(self.post(path, json_data=criteria)).get_data()
		return data


	def query_count(self, filters: dict) -> int:
		"""Count of projects matching given criteria

		Args:
			filters (dict): Filters for the query criteria

		Returns:
			int: Number of projects fitting the filters
		"""
		path = '/api/projects/query/count'
		criteria = self.__query_criteria(filters)
		data = JSONResponseHandler(self.post(path, json_data=criteria)).get_data()
		return data


	def project_status(self, project: int) -> dict:
		"""Provides information on all valid triage statuses for a project.

		Args:
			project (int): Project id

		Returns:
			dict: Project statuses
		"""
		path = f'/api/projects/{ project }/statuses'
		data = JSONResponseHandler(self.get(path)).get_data()
		return data


	def file_mappings(self, project: int, files: dict) -> dict:
		"""Provides source path mappings for a project.

		Args:
			project (int): Project id
			files (dict): Dictionary with files keyword and list of files

		Returns:
			dict: Contains the dictionary of file path mappings
		"""
		url = f'/api/projects/{ project }/files/mappings'
		data = JSONResponseHandler(self.post(url, json_data=files)).get_data()
		return data


	def project_files(self, project: int) -> list:
		"""Provides a list of files for a project.

		Args:
			project (int): Project id

		Returns:
			list: list of files
		"""
		path = f'/api/projects/{ project }/files'
		data = JSONResponseHandler(self.get(path)).get_data()
		return data


	def project_roles(self, project: int) -> list:
		"""Provides a list of all User roles.

		Args:
			project (int): project ID

		Returns:
			list: list of users and their roles for the project
		"""
		path = f'/api/projects/{ project }/user-roles'
		data = JSONResponseHandler(self.get(path)).get_data()
		return data


	def project_user(self, project: int, user: int) -> dict:
		"""Provides a User Role for a given user.

		Args:
			project (int): Project id
			user (int): User id

		Returns:
			dict: Contains the user role for the given user
		"""
		path = f'/api/projects/{ project }/user-roles/user/{ user }'
		data = JSONResponseHandler(self.get(path)).get_data()
		return data


	def update_user_role(self, project: int, user: int, roles: dict) -> None:
		"""Allows changing user roles.

		Note that you must specify the entire set of roles each time;
		if you fail to include a role when using this method,
		the user will lose that role.
		Args:
			project (int): Project id
			user (int): User id
			roles (dict): dictionary of user roles
		"""
		path = f'/api/projects/{ project }/user-roles/user/{ user }'
		ResponseHandler(self.put(path, json_data=roles)).validate()
		return


	def print_projects(self):
		"""Prints a sorted list of project names and ids."""
		print("Project (ID)\n==============")
		data = self.get_projects()
		projects = data['projects']
		for project in sorted(projects, key = lambda i: i['name']):
			name = project["name"]
			pid = project["id"]
			print(f"{ name } ({ pid })")


	def get_project_id(self, name: str) -> int:
		"""Gets the project id

		Args:
			name (str): Name of the project on CodeDx

		Returns:
			int: Project id
		"""
		filters = {
			"name": name
		}
		projects = self.query_projects(filters)
		project_id = next((project["id"] for project in projects if project["name"] == name), None)

		return project_id
