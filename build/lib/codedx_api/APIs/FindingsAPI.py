from enum import Enum
from typing import List

from codedx_api.APIs.BaseAPIClient import (BaseAPIClient,
                                           ContentResponseHandler, ContentType,
                                           JSONResponseHandler)


class FindingStatus(str, Enum):
	"""Enumeration of finding status types"""    
	FIXED = "fixed",
	MITIGATED = "mitigated",
	IGNORED = "ignored",
	FP = "false-positive",
	GONE = "gone",
	UNRESOLVED = "unresolved",
	ESCALATED = "escalated"


	def __contains__(cls, item):
		try:
			cls(item)
		except ValueError:
			return False
		return True    


	def __str__(self):
		return str(self.name).lower()

	def format(self) -> str:
		"""Get status in format that will be accepted by CodeDx

		Returns:
			str: Finding status
		"""
		return str(self.value)

	@classmethod
	def print_statuses(cls):
		"""Prints the list of statuses available on CodeDx (Feb 2021)"""	
		for status in cls:
			print(status)


class Findings(BaseAPIClient):

	def get_finding(self, finding: int, options: List[str] = None) -> dict:
		"""Returns metadata for the given finding

		Args:
			finding (int): Finding id
			options (List[str], optional): The expand parameter is a comma separated list, which can modify the reponse. Defaults to None.

		Returns:
			dict: [description]
		"""
		path = f"/api/findings/{ finding }"
		if options:
			expanders = ",".join(options)
			query = f'?expand={ expanders }'
			path += query
		data = JSONResponseHandler(self.get(path)).get_data()
		return data


	def get_finding_description(self, finding: int) -> dict:
		"""Returns the descriptions for the given finding from all available sources.

		Args:
			finding (int): Finding id

		Returns:
			dict: Contains the description(s) for the finding
		"""
		path = f"/api/findings/{ finding }/description"
		data = JSONResponseHandler(self.get(path)).get_data()
		return data


	def get_finding_history(self, finding: int) -> list:
		"""Responds with an array of "activity event" objects.

		Args:
			finding (int): Finding id

		Returns:
			list: An array of "activity event" objects
		"""
		path = f"/api/findings/{ finding }/history"
		data = JSONResponseHandler(self.get(path)).get_data()
		return data


	def get_finding_table(self, project: int, options: List[str] = None, req_body: dict = None) -> dict:
		"""Returns filtered finding table data.

		Args:
			project (int): Project id
			options (List[str], optional): The expand parameter is a comma separated list. Defaults to None.
			req_body (dict, optional): Filters, pagination options. Defaults to None.

		Returns:
			dict: [description]
		"""
		path = f"/api/projects/{ project }/findings/table"
		if options:
			query = "?expand=" + ",".join(options)
			path += query
		if not req_body: 
			req_body = {}
		data = JSONResponseHandler(self.post(path, json_data=req_body)).get_data()
		return data


	def get_finding_count(self, project: int, req_body: dict = None) -> dict:
		"""Returns the count of all findings in the project matching the given filter.

		Args:
			project (int): Project ID
			req_body (dict, optional): Filters, pagination options. Defaults to None.

		Returns:
			dict: Dictionary with project finding count
		"""
		path = f"/api/projects/{ project }/findings/count"
		if not req_body: req_body = {}
		data = JSONResponseHandler(self.post(path, json_data=req_body)).get_data()
		return data


	def get_finding_group_count(self, project: int, req_body: dict) -> list:
		"""Returns filtered finding counts, grouped by the specified field.

		Args:
			project (int): [description]
			req_body (dict): Dictionary with "countBy" key and filters.

		Returns:
			list: Grouped counts
		"""
		path = f"/api/projects/{ project }/findings/grouped-counts"
		data = JSONResponseHandler(self.post(path, json_data=req_body)).get_data()
		return data


	def get_finding_flow(self, project: int, req_body: dict) -> list:
		"""Returns filtered finding flow data.

		Args:
			project (int): Project ID
			req_body (dict): Filters
		Returns:
			list: Contains the filtered flow data
		"""
		path = f"/api/projects/{ project }/findings/flow"
		data = JSONResponseHandler(self.post(path, json_data=req_body)).get_data()
		return data


	def get_finding_file(self, project: int, path_id: int) -> str:
		"""Returns the contents of a given file, as long as it is a text file.

		Args:
			project (int): Project id
			path_id (int): Path id

		Returns:
			str: Contains the requested file's content
		"""
		path = f"/api/projects/{ project }/files/{ path_id }"
		data = ContentResponseHandler(self.get(path), ContentType.TEXT.text()).get_data()
		return data


	def get_finding_file(self, project: int, file_path: str) -> str:
		"""Returns the contents of a given file, as long as it is a text file.

		Args:
			project (int): Project id
			file_path (str): The literal path to the file

		Returns:
			str: Contains the requested file's content
		"""
		path = f"/api/projects/{ project }/files/tree/{ file_path }"
		data = ContentResponseHandler(self.get(path), ContentType.TEXT.text()).get_data()
		return data
