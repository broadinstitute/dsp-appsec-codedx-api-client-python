import time

from codedx_api.APIs import (ActionsAPI, AnalysisAPI, FindingsAPI, JobsAPI,
                             ProjectsAPI, ReportsAPI)
from codedx_api.APIs.BaseAPIClient import ContentType


class CodeDx(ProjectsAPI.Projects, ReportsAPI.Reports, JobsAPI.Jobs, AnalysisAPI.Analysis, ActionsAPI.Actions, FindingsAPI.Findings):


	def __init__(self, base, api_key):
		"""Create a codeDx APIclient."""
		super().__init__(base, api_key)


	def download_report(self, data: str, file_name: str) -> None:
		"""Write data to file

		Args:
			data (str): Data from CodeDx
			file_name (str): Name of file
		"""
		with open(file_name, 'wb') as f:
			f.write(data)


	def wait_for_job(self, job: dict, job_desc: str = "Waiting for job.") -> dict:
		"""Waits for job to complete.

		Args:
			job (dict): Job object from CodeDx.
			job_desc (str, optional): Message for debugging. Defaults to "Waiting for job.".

		Returns:
			dict: Job object
		"""
		while "status" not in job or job["status"] != "completed":
			print(job_desc)
			time.sleep(1)
			job = self.job_status(job["jobId"])
		return job


	def get_report(self, job: dict, content_type: ContentType, file_name: str) -> None:
		"""Given a report generation job, downloads a report.

		Args:
			job (dict): Job object for report generation
			content_type (ContentType): Report type
			file_name (str): Name of file for downloaded report
		"""		
		description = f"Waiting for { content_type } report generation."
		self.wait_for_job(job, description)
		print("Downloading report...")
		res = self.job_result(job["jobId"], content_type)
		self.download_report(res, file_name)
		return


	def get_pdf(self,
			project: str,
			summary_mode: str = "simple",
			details_mode: str = "with-source",
			include_result_details: bool = False,
			include_comments: bool = False,
			include_request_response: bool = False,
			file_name: str = 'report.pdf',
			filters: dict = None) -> None:
		"""Download a project report in PDF format.

		Args:
			project (str): CodeDx project name
			summary_mode (str, optional): Report summary type. Defaults to "simple".
			details_mode (str, optional): Report details. Defaults to "with-source".
			include_result_details (bool, optional): Include result details. Defaults to False.
			include_comments (bool, optional): Include comments. Defaults to False.
			include_request_response (bool, optional): Include HTTP requests/responses. Defaults to False.
			file_name (str, optional): Name for report file. Defaults to 'report.pdf'.
			filters (dict, optional): Report filters. Defaults to None.
		"""
		pid = self.get_project_id(project)
		if not filters:
			filters = {}
		job = self.generate_pdf(pid, summary_mode, details_mode, include_result_details, include_comments, include_request_response, filters)
		self.get_report(job, ContentType.PDF, file_name)
		return


	def get_csv(self, project: str, cols: list = None, file_name: str = 'report.csv') -> None:
		"""Download a project report in CSV format.

		Args:
			project (str): CodeDx project name
			cols (list[str], optional): List of columns, will include all columns in None specified. Defaults to None.
			file_name (str, optional): Name for report file. Defaults to 'report.csv'.
		"""		
		pid = self.get_project_id(project)
		if not cols: 
			cols = self.get_csv_columns()
		job = self.generate_csv(pid, cols)
		res = self.get_report(job, ContentType.CSV, file_name)
		return


	def get_xml(self,
		project: str,
		include_standards: bool = False,
		include_source: bool = False,
		include_rule_descriptions: bool = True,
		file_name: str = 'report.xml') -> None:
		"""Download a project report in XML format.

		Args:
			project (str): CodeDx project name
			include_standards (bool, optional): List standards violations. Defaults to False.
			include_source (bool, optional): Include source code snippets. Defaults to False.
			include_rule_descriptions (bool, optional): Include rule descriptions. Defaults to True.
			file_name (str, optional): Name for report file. Defaults to 'report.xml'.
		"""		 
		pid = self.get_project_id(project)
		job = self.generate_xml(pid, include_standards, include_source, include_rule_descriptions)
		self.download_report(job, file_name)
		return


	def get_nessus(self):
		pass


	def get_nbe(self):
		pass


	def analyze(self, project: str, file_name: str) -> dict:
		"""Upload a vulnerability scan and run an analysis.

		Args:
			project (str): CodeDx project name.
			file_name (str): File to upload.

		Raises:
			Exception: ValueError if there are errors in the file uploaded.

		Returns:
			dict: Analysis object.
		"""		
		print("Creating analysis...")
		pid = self.get_project_id(project)
		prep = self.create_analysis(pid)
		prep_id = prep["prepId"]
		print("Uploading report...")
		ext_analysis = self.upload_analysis(prep_id, file_name)
		self.wait_for_job(ext_analysis, "Analyzing external report content.")
		prep = self.get_prep(prep_id)
		if 'verificationErrors' in prep and len(prep['verificationErrors']) > 0:
			print("Verification Errors:")
			for error in prep['verificationErrors']:
				print(error)
			raise ValueError("Fix verification errors in external vulnerability report.")
		else:
			analysis_job = self.run_analysis(prep_id)
			self.wait_for_job(analysis_job, "Running analysis.")
			analysis = self.get_analysis(pid, analysis_job["analysisId"])
			print("Analysis complete.")
			return analysis


	def update_statuses(self, project: str, status: str = "false-positive", filters: dict = None) -> None:
		"""Update status of findings in a project.

		Args:
			project (str): CodeDx project name.
			status (str, optional): New issue status. Defaults to "false-positive".
			filters (dict, optional): Apply status to filtered findings. Defaults to None.
		"""		
		pid = self.get_project_id(project)
		if not filters:
			filters = {}
		print("Updating bulk statuses...")
		job = self.bulk_status_update(pid, status, filters)
		self.wait_for_job(job, "Waiting for statuses to update...")
		msg = "Bulk status update (%s) for project %s" % (status, project)
		print(msg)
