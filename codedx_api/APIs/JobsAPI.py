from codedx_api.APIs.BaseAPIClient import (BaseAPIClient,
                                           ContentResponseHandler, ContentType,
                                           JSONResponseHandler)


# Jobs API Client for Code DX Projects API
class Jobs(BaseAPIClient):


	def job_status(self, job: str) -> dict:
		"""Queries the status of a running job.

		Args:
			job (str): Job id

		Returns:
			dict: Job status
		"""
		path = f'/api/jobs/{ job }'
		data = JSONResponseHandler(self.get(path)).get_data()
		return data


	def job_result(self, job: str, accept: ContentType) -> str:
		"""Fetches the result from a job.

		Args:
			job (str): Job ID
			accept (ContentType): Job content type

		Returns:
			str: Job result is returned - the response headers and body will match the job result
		"""
		path = f'/api/jobs/{ job }/result'
		data = ContentResponseHandler(self.download(path), accept).get_data()
		return data
