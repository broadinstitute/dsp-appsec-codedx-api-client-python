from apiclient.APIs import ProjectsAPI, ReportsAPI, JobsAPI, AnalysisAPI
import time, os

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

class CodeDX(ProjectsAPI.Projects, ReportsAPI.Reports, JobsAPI.Jobs, AnalysisAPI.Analysis):
	def __init__(self, base, api_key, verbose=False):
		super().__init__(base, api_key, verbose)

	def download_report(self, data, file_name):
		""" Saves the report in a file.
		"""
		self.type_check(file_name, str, "Filename")
		print(os.getcwd())
		try:
			print("using wb permissions")
			with open(file_name, 'wb') as f:
					f.write(data)
		except:
			try:
				print("using w+ permissions")
				with open(file_name, 'w+') as f:
						f.write(data)
			except:
				try:
					print("adding dir to filename")
					fn = '~/reports/' + file_name
					with open(fn, 'wb') as f:
							f.write(data)
				except:
					try:
						print("adding dir to filename w+")
						fn = '~/reports/' + file_name
						with open(fn, 'w+') as f:
								f.write(data)
					except:
						print("none worked")

	def get_report(self, job, content_type, file_name, msg):
		""" Get the project report from Code DX
		"""
		self.wait_for_job(job, msg)
		print("Downloading report...")
		res = self.job_result(job["jobId"], content_type)
		self.download_report(res, file_name)
		return res

	def wait_for_job(self, job, msg):
		job["status"] = "queued"
		while job["status"] != "completed":
			print(msg)
			time.sleep(1)
			job = self.job_status(job["jobId"])
		return job

	def get_pdf(self, proj, summary_mode="simple", details_mode="with-source", include_result_details=False, include_comments=False, include_request_response=False, file_name='report.pdf'):
		""" Download a project report in PDF format.
		"""
		job = self.generate_pdf(proj, summary_mode, details_mode, include_result_details, include_comments, include_request_response)
		res = self.get_report(job, 'application/pdf', file_name, "Waiting for report generation...")
		return res

	def get_csv(self, proj, cols=report_columns, file_name='report.csv'):
		""" Download a project report in CSV format.
		"""
		job = self.generate_csv(proj, cols)
		res = self.get_report(job, 'text/csv', file_name, "Waiting for report generation...")
		return res

	def get_xml(self, proj, include_standards=False, include_source=False, include_rule_descriptions=True, file_name='report.xml'):
		""" Allows user to queue a job to generate an xml report. Returns jobId and status.
			include_standards <Boolean>: List standards violations. Default is fault.
			include_source <Boolean>: Include source code snippets. Default is false.
			include_rule_descriptions <Boolean>: Include rule descriptions. Default is true.
		"""
		job = self.generate_xml(proj, include_standards, include_source, include_rule_descriptions)
		res = self.download_report(job, 'text/xml', file_name)
		return res

	def get_nessus():
		pass

	def get_nbe():
		pass

	def analyze(self, proj, file_name):
		""" Upload a vulnerability scan and run an analysis
		"""
		print("Creating analysis...")
		prep = self.create_analysis(proj)
		prep_id = prep["prepId"]
		print("Uploading report...")
		ext_analysis = self.upload_analysis(prep_id, file_name)
		self.wait_for_job(ext_analysis, "Analyzing external report content...")
		prep = self.get_prep(prep_id)
		if 'verificationErrors' in prep and len(prep['verificationErrors']) > 0:
			print("Verification Errors:")
			for error in prep['verificationErrors']:
				print(error)
			raise Exception("Fix verification errors...")
		else:
			analysis_job = self.run_analysis(prep_id)
			job = self.wait_for_job(analysis_job, "Running analysis...")
			analysis = self.get_analysis(proj, analysis_job["analysisId"])
			print("Analysis complete.")
			return analysis



		