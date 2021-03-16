from codedx_api.APIs.BaseAPIClient import BaseAPIClient, JSONResponseHandler
from codedx_api.APIs.FindingsAPI import FindingStatus
from codedx_api.APIs.ProjectsAPI import Projects


# Actions API Client for Code DX Projects API
class Actions(BaseAPIClient):

	def bulk_status_update(self, project: int, status: str, filters : dict = None) -> dict:
		"""Applies a status to a group of findings in a project based on project id

		Args:
			project (int): Project id
			status (str): New finding status
			filters (dict, optional): Filters the group of findings. Defaults to None.

		Returns:
			dict: Job object from CodeDx
		"""	
		if filters == None:
			filters = {}
		FindingStatus(status)
		path = f"/api/projects/{ project }/bulk-status-update"
		params = {
			"filter": filters,
			"status": status
		}
		data = JSONResponseHandler(self.post(path, params)).get_data()
		return data
