import re

from codedx_api.APIs.BaseAPIClient import BaseAPIClient, JSONResponseHandler
from codedx_api.APIs.ProjectsAPI import Projects


# Reports Client for Code DX Projects API
class Reports(BaseAPIClient):
	def __init__(self, base, api_key):
		""" Creates an API Client for Code DX Projects API

			Args:
				base: String representing base url from Code DX
				api_key: String representing API key from Code DX
				verbose: Boolean - not supported yet

		"""
		super().__init__(base, api_key)
		self.report_columns = [
			"projectHierarchy",
			"id",
			"creationDate",
			"updateDate",
			"severity",
			"status",
			"cwe",
			"rule",
			"tool",
			"location",
			"element",
			"loc.path",
			"loc.line"
		]
		self.projects_api = Projects(base, api_key)

	def report_types(self, project: int) -> dict:
		"""Provides a list of report types for a project.

		Args:
			project (int): Project id

		Returns:
			dict: Report types and report configuration options
		"""
		path = f'/api/projects/{ project }/report/types'
		data = JSONResponseData(self.get(path)).get_data()
		return data

	def generate(self, project: int, report_type: str, config: dict, filters: dict = None) -> dict:
		"""Allows user to queue a job to generate a report.

		Args:
			project (int): Project id
			report_type (str): Report type
			config (dict): Report configuration options
			filters (dict, optional): Filters for findings in report. Defaults to None.

		Returns:
			dict: Data about the queued reporting task wth jobId and inputID
		"""
		params = {
			"config": config
		}
		if filters:
			params["filter"] = filters
		path = f'/api/projects/{ project }/report/{ report_type }'
		data = JSONResponseHandler(self.post(path, json_data=params)).get_data()
		return data

	def generate_pdf(self,
		project: int,
		summary_mode: str = "simple",
		details_mode: str = "with-source",
		include_result_details: bool = False,
		include_comments: bool = False,
		include_request_response: bool = False,
		filters: dict = None) -> dict:
		"""Allows user to queue a job to generate a PDF report. 

		Args:
			project (int): CodeDx project id
			summary_mode (str, optional): Summary mode. Defaults to "simple".
			details_mode (str, optional): Details mode. Defaults to "with-source".
			include_result_details (bool, optional): Include result details. Defaults to False.
			include_comments (bool, optional): Include comments. Defaults to False.
			include_request_response (bool, optional): Include HTTP requests/responses. Defaults to False.
			filters (dict, optional): Filter findings in the reports. Defaults to None.

		Raises:
			RuntimeError: Invalid summary mode input.
			RuntimeError: Invalid details mode input.

		Returns:
			dict: Data about the queued reporting task wth jobId and inputID
		"""		
		if not filters: 
			filters = {}
		if summary_mode not in ["none", "simple", "detailed"]: 
			raise RuntimeError("Invalid summary mode input.")
		if details_mode not in ["none", "simple", "with-source"]: 
			raise RuntimeError("Invalid details mode input given.")
		config = {
			"summaryMode": summary_mode,
			"detailsMode": details_mode,
			"includeResultDetails": include_result_details,
			"includeComments": include_comments,
			"includeRequestResponse": include_request_response
		}
		data = self.generate(project, "pdf", config, filters)
		return data

	def get_csv_columns(self) -> list:
		"""Returns a list of optional columns for a project csv report."""
		return self.report_columns

	def generate_csv(self, project: int,  cols: list = None) -> dict:
		"""Allows user to queue a job to generate a CSV report.

		Args:
			project (int): CodeDx project id.
			cols (list, optional): Columns to include in CSV report. Defaults to None.

		Returns:
			dict: Data about the queued reporting task wth jobId and inputID
		"""
		if not cols: 
			cols = self.report_columns
		config = {
			"columns": cols
		}
		config["columns"] = cols
		data = self.generate(project, "csv", config)
		return data

	def generate_xml(self,
		project: int,
		include_standards: bool = False,
		include_source: bool = False,
		include_rule_descriptions: bool = True) -> dict:
		"""Allows user to queue a job to generate a XML report.

		Args:
			project (int): CodeDx project id.
			include_standards (bool, optional): Include standards. Defaults to False.
			include_source (bool, optional): Include source. Defaults to False.
			include_rule_descriptions (bool, optional): Include rule descriptions. Defaults to True.

		Returns:
			dict: Data about the queued reporting task wth jobId and inputID
		"""
		config = {
			"includeStandards": include_standards,
			"includeSource": include_source,
			"includeRuleDescriptions": include_rule_descriptions
		}
		data = self.generate(project, "xml", config)
		return data

	def generate_nessus(self,
		project: int,
		default_host: str = None,
		operating_system: str = "",
		mac_address: str = "",
		netBIOS_name: str = "") -> dict:
		"""Allows user to queue a job to generate a Nessus report.

		Args:
			project (int): CodeDx project id.
			default_host (str, optional): Default host. Defaults to None.
			operating_system (str, optional): Operating system. Defaults to "".
			mac_address (str, optional): MAC address. Defaults to "".
			netBIOS_name (str, optional): netBIOS name. Defaults to "".

		Raises:
			RuntimeError: Raise if given an invalid mac address.

		Returns:
			dict: Data about the queued reporting task wth jobId and inputID
		"""		
		if re.search(mac_address, "^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$") is None:
			raise RuntimeError("Nessus report not given a valid mac address.")
		config = {
			"defaultHost": default_host,
			"operatingSystem": operating_system,
			"macAddress": mac_address,
			"netBIOSName": netBIOS_name
		}
		data = self.generate(project, "nessus", config)
		return data

	def generate_nbe(self, project: int, host_address: str = None) -> dict:
		"""Allows user to queue a job to generate a NBE report.

		Args:
			project (int): CodeDx project id.
			host_address (str, optional): IP address. Defaults to None.

		Raises:
			RuntimeError: Given an invalid host address
		Returns:
			dict: Data about the queued reporting task wth jobId and inputID
		"""		
		if re.search(host_address, "^((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\\.){3}((25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9]))$") is None:
			raise RuntimeError("NBE report not given a valid IPv4 address.")
		config = {
			"hostAddresss": host_address
		}
		data = self.generate(project, "nbe", config)
		return data
