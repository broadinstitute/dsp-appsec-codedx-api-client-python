import unittest
import os
from unittest.mock import MagicMock, patch
from apiclient.APIs import UsersAPI

# DO NOT UPDATE - MOCK REQUESTS DO NOT REQUIRE CREDENTIALS
api_key = "0000-0000-0000-0000"
base_url = "https://[CODE_DX_BASE_URL].org/codedx"

class UsersAPI_test(unittest.TestCase):

	def setUp(self):
		unittest.TestCase.setUp(self)
		self.users_api = UsersAPI.User(api_key, base_url)