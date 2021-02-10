from codedx_api.APIs.BaseAPIClient import BaseAPIClient
from codedx_api.APIs.ProjectsAPI import Projects

class Findings(BaseAPIClient):
	def __init__(self, base, api_key, verbose = False):
		"""Iniitilize"""
		super().__init__(base, api_key, verbose)
		self.projects_api = Projects(base, api_key)

	def get_finding(self, fid, options=None):
		""" Returns metadata for the given finding.

			Can include a list of optional expanders to include more information
			Available values: descriptions, descriptor, issue, triage-time, results, results.descriptions, results.descriptor, results.metadata, results.variants

			Args:
				fid: finding id
				options: additional information on finding

			Output:
				response

		"""
		self.type_check(fid, int, "Findings ID")
		local_url = f"/api/findings/{ fid }"
		if options:
			self.type_check(options, list, "Optional expanders")
			query = "?expand=" + ",".join(options)
			local_url += query
		res = self.call("GET", local_url)
		return res

	def get_finding_description(self, fid):
		""" Returns the descriptions for the given finding from all available sources.

			Args:
				fid: finding id

			Output:
				response

		"""
		self.type_check(fid, int, "Findings ID")
		local_url = f"/api/findings/{ fid }/description"
		res = self.call("GET", local_url)
		return res

	def get_finding_history(self, fid):
		""" Responds with an array of “activity event” objects in JSON.

			Args:
				fid: finding id

			Output:
				response

		"""
		self.type_check(fid, int, "Findings ID")
		local_url = f"/api/findings/{ fid }/history"
		res = self.call("GET", local_url)
		return res

	def get_finding_table(self, proj, options=None, req_body=None):
		""" Returns filtered finding table data.

			This endpoint is a candidate to become a more generic querying API; presently it just returns the data required for the findings table as it exists today.

			Args:
				fid: finding id
				options: additional information on finding
				query: query info

			Output:
				response

		"""
		self.projects_api.update_projects()
		pid = self.projects_api.process_project(proj)
		local_url = f"/api/projects/{ pid }/findings/table"
		if options:
			self.type_check(options, list, "Optional expanders")
			query = "?expand=" + ",".join(options)
			local_url += query
		if not req_body: req_body = {}
		res = self.call("POST", local_path=local_url, json_data=req_body)
		return res
		

	def get_finding_count(self, proj, req_body=None):
		""" Returns the count of all findings in the project matching the given filter.

			Args:
				proj: project name or id
				query: query info

			Output:
				response

		"""
		self.projects_api.update_projects()
		pid = self.projects_api.process_project(proj)
		local_url = f"/api/projects/{ pid }/findings/count"
		if not req_body: req_body = {}
		res = self.call("POST", local_path=local_url, json_data=req_body)
		return res

	def get_finding_group_count(self, proj, req_body=None):
		""" Returns filtered finding table data.

			This endpoint is a candidate to become a more generic querying API; presently it just returns the data required for the findings table as it exists today.

			Args:
				proj: project name or id
				query: query info

			Output:
				response

		"""
		self.projects_api.update_projects()
		pid = self.projects_api.process_project(proj)
		local_url = f"/api/projects/{ pid }/findings/grouped-counts"
		if not req_body: req_body = {}
		res = self.call("POST", local_path=local_url, json_data=req_body)
		return res

	def get_finding_flow(self, proj, req_body=None):
		""" Returns filtered finding table data.

			This endpoint is a candidate to become a more generic querying API; presently it just returns the data required for the findings table as it exists today.

			Args:
				proj: project name or id
				flow_req: See CodedX API

			Output:
				response

		"""
		self.projects_api.update_projects()
		pid = self.projects_api.process_project(proj)
		local_url = f"/api/projects/{ pid }/findings/flow"
		if not req_body: req_body = {}
		res = self.call("POST", local_path=local_url, json_data=req_body)
		return res

	def get_finding_file(self, proj, path):
		""" Returns the contents of a given file, as long as it is a text file.

			Args:
				proj: project name or id
				path: path to codedx file - string or int

			Output:
				response

		"""
		self.projects_api.update_projects()
		pid = self.projects_api.process_project(proj)
		if isinstance(path, str):
			local_url = f"/api/projects/{ pid }/files/tree/{ path }"
		elif isinstance(path, int):
			local_url = f"/api/projects/{ pid }/files/{ path }"
		else:
			raise Exception("File path must be either string or int.")
		res = self.call("GET", local_url)
		return res
