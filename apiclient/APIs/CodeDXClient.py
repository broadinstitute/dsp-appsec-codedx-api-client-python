from apiclient.APIs import ProjectsAPI, ReportsAPI, JobsAPI
import time

report_columns = [
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

class CodeDX(ProjectsAPI.Projects, ReportsAPI.Reports, JobsAPI.Jobs):
	def __init__(self, base, api_key, verbose=False):
		super().__init__(base, api_key, verbose)

	def save_report(self, data, file_name):
		self.type_check(file_name, str, "Filename")
		with open(file_name, 'wb') as f:
				f.write(data)

	def download_report(self, job, content_type, file_name):
		job["status"] = "queued"
		while job["status"] != "completed":
			print("Waiting for report generation...")
			time.sleep(1)
			job = self.job_status(job["jobId"])
		print("Downloading report...")
		res = self.job_result(job["jobId"], content_type)
		self.save_report(res, file_name)
		return res

	def get_pdf(self, proj, summary_mode="simple", details_mode="with-source", include_result_details=False, include_comments=False, include_request_response=False, file_name='report.pdf'):
		job = self.generate_pdf(proj, summary_mode, details_mode, include_result_details, include_comments, include_request_response)
		res = self.download_report(job, 'application/pdf', file_name)
		return res

	def get_csv(self, proj, cols=report_columns, file_name='report.csv'):
		job = self.generate_csv(proj, cols)
		res = self.download_report(job, 'text/csv', file_name)
		return res

	def get_xml():
		pass

	def get_nessus():
		pass

	def get_nbe():
		pass

		