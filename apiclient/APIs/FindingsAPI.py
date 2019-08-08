from apiclient.apiclient import APIClient

class Findings(APIClient):
	
	def __init__(self, base, api_key, verbose = False):
		super().__init__(base, api_key, verbose)

	
