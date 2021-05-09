import os
from typing import List

from codedx_api.APIs.BaseAPIClient import (BaseAPIClient, JSONResponseHandler,
                                           ResponseHandler)


# Jobs API Client for Code DX Projects API
class Analysis(BaseAPIClient):


	def __get_file_data(self, file_name):
		file_ext = os.path.splitext(file_name)[1]
		accepted_file_types = {
			'.xml': 'text/xml',
			'.json': 'application/json',
			'.zip': 'application/zip',
			'.csv': 'text/csv',
			'.txt': 'text/plain'
		}
		file_data = {
			'file_name': file_name,
			'file_path': file_name,
			'file_type': accepted_file_types[file_ext]
		}
		return file_data


	def create_analysis(self, project: int) -> dict:
		"""Create a new Analysis Prep associated with a particular project.

		Args:
			project (int): project id

		Returns:
			dict: new Analysis Prep as JSON
		"""
		path = '/api/analysis-prep'
		params = {"projectId": project}
		data = JSONResponseHandler(self.post(path, params)).get_data()
		return data


	def get_prep(self, prep_id: str) -> dict:
		"""Get lists of Input IDs and Verification Errors for an Analysis Prep.

		Args:
			prep_id (str): Analysis Prep id

		Returns:
			dict: input ids and verification errors
		"""
		path = f'/api/analysis-prep/{ prep_id }'
		data = JSONResponseHandler(self.get(path)).get_data()
		return data


	def upload_analysis(self, prep_id: str, file_name: str, client_request_id: str = None) -> dict:
		"""Analysis Preps should be populated by uploading files to Code Dx.

		This will create a job to determine the contents of the file.
		Args:
			prep_id (str): Analysis Prep ID
			file_name (str): File for analysis
			client_request_id (str, optional): Arbitrary identifier used to make modifications to analysis later. Defaults to None.

		Returns:
			dict: Data about the job created
		"""
		path = f'/api/analysis-prep/{ prep_id }/upload'
		file_data = self.__get_file_data(file_name)
		if client_request_id:
			headers['X-Client-Request-Id'] = client_request_id
		data = JSONResponseHandler(self.upload(path, file_data=file_data)).get_data()
		return data


	def get_input_metadata(self, prep_id: str, input_id: str) -> dict:
		"""[summary]

		Args:
			prep_id (str): Prep ID
			input_id (str): Input ID

		Returns:
			dict: Input data
		"""
		path = f'/api/analysis-prep/{ prep_id }/{ input_id }'
		data = JSONResponseHandler(self.get(path)).get_data()
		return data


	def delete_input(self, prep_id: str, input_id: str):
		"""Delete an input

		Args:
			prep_id (str): Prep ID
			input_id (str): Input ID
		"""
		path = f'/api/analysis-prep/{ prep_id }/{ input_id }'
		ResponseHandler(self.delete(path)).validate()
		return


	def delete_pending(self, prep_id: str, client_request_id: str):
		"""Delete input that is still pending and has no input ID yet

		Args:
			prep_id (str): Prep ID
			client_request_id (str): X-Client-Request-Id used to upload input
		"""
		path = '/api/analysis-prep/%s/pending' % prep_id
		headers = {'X-Client-Request-Id': client_request_id}
		ResponseHandler(self.delete(path, local_headers=headers)).validate()
		return


	def toggle_display_tag(self, prep_id: str, input_id: str, tag_id: str, enabled: bool) -> dict:
		"""Enable and disable individual display tags on individual prop inputs.

		Args:
			prep_id (str): Prep ID
			input_id (str): Input ID
			tag_id (str): Tag ID
			enabled (bool): True to enable, False to disable

		Returns:
			dict: Input Display Info object as JSON, representing the new state of the input
		"""
		path = f'/api/analysis-prep/{ prep_id }/{ input_id }/tag/{ tag_id }'
		params = {"enabled": enabled}
		data = JSONResponseHandler(self.put(path, json_data=params)).get_data()
		return data


	def run_analysis(self, prep_id: str) -> dict:
		"""Start an analysis

		Args:
			prep_id (str): Analysis prep id

		Returns:
			dict: Analysis ID and Job ID for analysis
		"""
		path = f'/api/analysis-prep/{ prep_id }/analyze'
		data = JSONResponseHandler(self.post(path)).get_data()
		return data


	def upload_run_analysis(self, project: int, file_names: List[str]) -> dict:
		pass

	def get_all_analysis(self, project: int) -> list:
		"""Get list of analysis details for analysis associated with a project

		Args:
			project (int): Project ID

		Returns:
			list: List of analysis details
		"""
		path = f'/api/projects/{ project }/analyses'
		data = JSONResponseHandler(self.get(path)).get_data()
		return data

	def get_analysis(self, project: int, analysis: int) -> dict:
		"""Obtain analysis details, such as start and finish times

		Args:
			project (int): Project ID
			analysis (int): Analysis ID

		Returns:
			dict: Analysis details
		"""
		path = f'/api/projects/{ project }/analyses/{ analysis }'
		data = JSONResponseHandler(self.get(path)).get_data()
		return data

	def name_analysis(self, project: int, analysis: int, name: str):
		"""Set a name for a specific analysis

		Args:
			project (int): Project ID
			analysis (int): Analysis ID
			name (str): New analysis name
		"""
		path = f'/api/projects/{ project }/analyses/{ analysis }'
		params = {"name": name}
		ResponseHandler(self.put(path, json_data=params)).validate()
		return


	def enable_display_tag(self, prep_id: str, input_id: str, tag_id: str) -> dict:
		"""Enable an individual display tag on individual prop inputs.

		Args:
			prep_id (str): Prep ID
			input_id (str): Input ID
			tag_id (str): Tag

		Returns:
			dict: Input Display Info object as JSON, representing the new state of the input
		"""
		res = self.toggle_display_tag(prep_id, input_id, tag_id, True)
		return res

	def disable_display_tag(self, prep_id: str, input_id: str, tag_id: str) -> dict:
		"""Disable an individual display tag on individual prop inputs.

		Args:
			prep_id (str): Prep ID
			input_id (str): Input ID
			tag_id (str): Tag

		Returns:
			dict: Input Display Info object as JSON, representing the new state of the input
		"""
		data = self.toggle_display_tag(prep_id, input_id, tag_id, False)
		return data	
