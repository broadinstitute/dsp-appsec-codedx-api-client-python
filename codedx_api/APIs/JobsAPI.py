from codedx_api.APIs.BaseAPIClient import (BaseAPIClient,
                                           ContentResponseHandler,
                                           JSONResponseHandler)


# Jobs API Client for Code DX Projects API
class Jobs(BaseAPIClient):
	def __init__(self, base, api_key):
		""" Creates an API Client for Code DX Jobs API

			Args:
				base: String representing base url from Code DX
				api_key: String representing API key from Code DX
				verbose: Boolean - not supported yet

		"""
		super().__init__(base, api_key)


	def job_status(self, jid):
		"""Queries the status of a job."""
		self.type_check(jid, str, "JobId")
		local_url = '/api/jobs/%s' % jid
		data = JSONResponseHandler(self.get(local_url)).get_data()
		return data

	def job_result(self, jid, accept):
		"""Get the result of a job."""
		local_url = '/api/jobs/%s/result' % jid
		data = ContentResponseHandler(self.download(local_url), accept).get_data()
		return data
