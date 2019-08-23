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
		self.users_api = UsersAPI.Users(api_key, base_url)

	@patch('requests.post')
	def test_create_user(self, mock_create_user):
		mock_create_user.return_value.json.return_value = {
															"id": 0,
															"type": "local",
															"name": "string",
															"principal": "string",
															"isEnabled": True,
															"isSystem": True,
															"isAdmin": True,
															"isCurrent": True
														}
		mock_create_user.return_value.status_code = 200
		mock_create_user.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.users_api.create_user("new_user", "new_password", True, "Local")
		self.assertEqual(result["id"], 0)
		with self.assertRaises(Exception):
			self.users_api.create_user(None, "string", True, "Local")
		with self.assertRaises(Exception):
			self.users_api.create_user("string", None, True, "Local")
		with self.assertRaises(Exception):
			self.users_api.create_user("string", "string", True, "user")
		with self.assertRaises(Exception):
			self.users_api.create_user("string", "string", "true", "Local")

	@patch('requests.get')
	def test_get_users(self, mock_get_all_users):
		mock_get_all_users.return_value.json.return_value = [{
															"id": 0,
															"type": "local",
															"name": "string",
															"principal": "string",
															"isEnabled": True,
															"isSystem": True,
															"isAdmin": True,
															"isCurrent": True
														}]
		mock_get_all_users.return_value.status_code = 200
		mock_get_all_users.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.users_api.get_users()
		self.assertEqual(result[0]["id"], 0)
		result = self.users_api.get_users('LDAP')
		self.assertEqual(result[0]["id"], 0)
		with self.assertRaises(Exception):
			self.users_api.get_users("test")

	@patch('requests.get')
	def test_get_user(self, mock_get_all_users):
		test_uid = 5
		mock_get_all_users.return_value.json.return_value = [{
															"id": test_uid,
															"type": "local",
															"name": "string",
															"principal": "string",
															"isEnabled": True,
															"isSystem": True,
															"isAdmin": True,
															"isCurrent": True
														}]
		mock_get_all_users.return_value.status_code = 200
		mock_get_all_users.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.users_api.get_user(test_uid)
		self.assertEqual(result["id"], test_uid)
		with self.assertRaises(Exception):
			self.users_api.get_user(-1)

	@patch('requests.post')
	def test_create_local(self, mock_create_local):
		mock_create_local.return_value.json.return_value = {
															"id": 0,
															"type": "local",
															"name": "string",
															"principal": "string",
															"isEnabled": True,
															"isSystem": True,
															"isAdmin": True,
															"isCurrent": True
														}
		mock_create_local.return_value.status_code = 200
		mock_create_local.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.users_api.create_local("test", "test", True)
		self.assertEqual(result["id"], 0)
		self.assertEqual(result["type"], "local")
		with self.assertRaises(Exception):
			self.users_api.create_local("test", "test", None)

	@patch('requests.get')
	def test_get_locals(self, mock_get_locals):
		mock_get_locals.return_value.json.return_value = [{
															"id": 0,
															"type": "local",
															"name": "string",
															"principal": "string",
															"isEnabled": True,
															"isSystem": True,
															"isAdmin": True,
															"isCurrent": True
														}]
		mock_get_locals.return_value.status_code = 200
		mock_get_locals.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.users_api.get_locals()
		self.assertEqual(result[0]["id"], 0)
		self.assertEqual(result[0]["type"], "local")
		self.assertEqual(len(result), 1)

	@patch('requests.post')
	def test_create_ldap(self, mock_create_ldap):
		mock_create_ldap.return_value.json.return_value = {
															"id": 0,
															"type": "ldap",
															"name": "string",
															"principal": "string",
															"isEnabled": True,
															"isSystem": True,
															"isAdmin": True,
															"isCurrent": True
														}
		mock_create_ldap.return_value.status_code = 200
		mock_create_ldap.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.users_api.create_ldap("test", "test", True)
		self.assertEqual(result["id"], 0)
		self.assertEqual(result["type"], "ldap")
		with self.assertRaises(Exception):
			self.users_api.create_ldap("test", "test", None)

	@patch('requests.get')
	def test_get_ldap(self, mock_get_ldap):
		mock_get_ldap.return_value.json.return_value = [{
															"id": 0,
															"type": "ldap",
															"name": "string",
															"principal": "string",
															"isEnabled": True,
															"isSystem": True,
															"isAdmin": True,
															"isCurrent": True
														}]
		mock_get_ldap.return_value.status_code = 200
		mock_get_ldap.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.users_api.get_ldaps()
		self.assertEqual(result[0]["id"], 0)
		self.assertEqual(result[0]["type"], "ldap")
		self.assertEqual(len(result), 1)

	@patch('requests.post')
	def test_create_external(self, mock_create_external):
		mock_create_external.return_value.json.return_value = {
															"id": 0,
															"type": "external",
															"name": "string",
															"principal": "string",
															"isEnabled": True,
															"isSystem": True,
															"isAdmin": True,
															"isCurrent": True
														}
		mock_create_external.return_value.status_code = 200
		mock_create_external.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.users_api.create_external("test", "test", True)
		self.assertEqual(result["id"], 0)
		self.assertEqual(result["type"], "external")
		with self.assertRaises(Exception):
			self.users_api.create_external("test", "test", None)

	@patch('requests.get')
	def test_get_external(self, mock_get_external):
		mock_get_external.return_value.json.return_value = [{
															"id": 0,
															"type": "external",
															"name": "string",
															"principal": "string",
															"isEnabled": True,
															"isSystem": True,
															"isAdmin": True,
															"isCurrent": True
														}]
		mock_get_external.return_value.status_code = 200
		mock_get_external.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.users_api.get_externals()
		self.assertEqual(result[0]["id"], 0)
		self.assertEqual(result[0]["type"], "external")
		self.assertEqual(len(result), 1)

	@patch('requests.post')
	def test_create_key(self, mock_create_key):
		mock_create_key.return_value.json.return_value = {
															"id": 0,
															"type": "key",
															"name": "string",
															"principal": "string",
															"isEnabled": True,
															"isSystem": True,
															"isAdmin": True,
															"isCurrent": True
														}
		mock_create_key.return_value.status_code = 200
		mock_create_key.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.users_api.create_key("test", "test", True)
		self.assertEqual(result["id"], 0)
		self.assertEqual(result["type"], "key")
		with self.assertRaises(Exception):
			self.users_api.create_key("test", "test", None)

	@patch('requests.get')
	def test_get_key(self, mock_get_key):
		mock_get_key.return_value.json.return_value = [{
															"id": 0,
															"type": "key",
															"name": "string",
															"principal": "string",
															"isEnabled": True,
															"isSystem": True,
															"isAdmin": True,
															"isCurrent": True
														}]
		mock_get_key.return_value.status_code = 200
		mock_get_key.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.users_api.get_keys()
		self.assertEqual(result[0]["id"], 0)
		self.assertEqual(result[0]["type"], "key")
		self.assertEqual(len(result), 1)

	@patch('requests.put')
	def test_user_settings(self, mock_user_settings):
		mock_user_settings.return_value.json.return_value = {
																"id": 0,
																"type": "local",
																"name": "string",
																"principal": "string",
																"isEnabled": True,
																"isSystem": True,
																"isAdmin": True,
																"isCurrent": True
															}
		mock_user_settings.return_value.status_code = 200
		mock_user_settings.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.users_api.user_settings(0, True, False)
		self.assertEqual(result["id"], 0)
		with self.assertRaises(Exception):
			self.users_api.user_settings(None, True, False)
		with self.assertRaises(Exception):
			self.users_api.user_settings(0, None, False)
		with self.assertRaises(Exception):
			self.users_api.user_settings(0, False, None)

	@patch('requests.get')		
	@patch('requests.put')
	def test_enable_admin(self, mock_enable_admin, mock_users):
		test_uid = 5
		mock_enable_admin.return_value.json.return_value = {
																"id": test_uid,
																"type": "local",
																"name": "string",
																"principal": "string",
																"isEnabled": True,
																"isSystem": True,
																"isAdmin": True,
																"isCurrent": True
															}
		mock_enable_admin.return_value.status_code = 200
		mock_enable_admin.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		mock_users.return_value.status_code = 200
		mock_users.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		mock_users.return_value.json.return_value = [{
														"id": test_uid,
														"type": "local",
														"name": "string",
														"principal": "string",
														"isEnabled": True,
														"isSystem": True,
														"isAdmin": True,
														"isCurrent": True
													}]
		result = self.users_api.enable_admin(test_uid)
		self.assertTrue(result["isAdmin"])
		self.assertEqual(result["id"], test_uid)
		with self.assertRaises(Exception):
			self.users_api.enable_admin(-1)

	@patch('requests.get')		
	@patch('requests.put')
	def test_disable_admin(self, mock_disable_admin, mock_users):
		test_uid = 5
		mock_disable_admin.return_value.json.return_value = {
																"id": test_uid,
																"type": "local",
																"name": "string",
																"principal": "string",
																"isEnabled": True,
																"isSystem": True,
																"isAdmin": False,
																"isCurrent": True
															}
		mock_disable_admin.return_value.status_code = 200
		mock_disable_admin.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		mock_users.return_value.status_code = 200
		mock_users.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		mock_users.return_value.json.return_value = [{
														"id": test_uid,
														"type": "local",
														"name": "string",
														"principal": "string",
														"isEnabled": True,
														"isSystem": True,
														"isAdmin": True,
														"isCurrent": True
													}]
		result = self.users_api.disable_admin(test_uid)
		self.assertFalse(result["isAdmin"])
		self.assertEqual(result["id"], test_uid)
		with self.assertRaises(Exception):
			self.users_api.disable_admin(-1)

	@patch('requests.get')		
	@patch('requests.put')
	def test_enable_user(self, mock_enable_user, mock_users):
		test_uid = 5
		mock_enable_user.return_value.json.return_value = {
																"id": test_uid,
																"type": "local",
																"name": "string",
																"principal": "string",
																"isEnabled": True,
																"isSystem": True,
																"isAdmin": False,
																"isCurrent": True
															}
		mock_enable_user.return_value.status_code = 200
		mock_enable_user.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		mock_users.return_value.status_code = 200
		mock_users.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		mock_users.return_value.json.return_value = [{
														"id": test_uid,
														"type": "local",
														"name": "string",
														"principal": "string",
														"isEnabled": True,
														"isSystem": True,
														"isAdmin": False,
														"isCurrent": True
													}]
		result = self.users_api.enable_user(test_uid)
		self.assertTrue(result["isEnabled"])
		self.assertEqual(result["id"], test_uid)
		with self.assertRaises(Exception):
			self.users_api.enable_user(-1)

	@patch('requests.get')		
	@patch('requests.put')
	def test_disable_user(self, mock_disable_user, mock_users):
		test_uid = 5
		mock_disable_user.return_value.json.return_value = {
																"id": test_uid,
																"type": "local",
																"name": "string",
																"principal": "string",
																"isEnabled": False,
																"isSystem": True,
																"isAdmin": False,
																"isCurrent": True
															}
		mock_disable_user.return_value.status_code = 200
		mock_disable_user.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		mock_users.return_value.status_code = 200
		mock_users.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		mock_users.return_value.json.return_value = [{
														"id": test_uid,
														"type": "local",
														"name": "string",
														"principal": "string",
														"isEnabled": True,
														"isSystem": True,
														"isAdmin": False,
														"isCurrent": True
													}]
		result = self.users_api.disable_user(test_uid)
		self.assertFalse(result["isEnabled"])
		self.assertEqual(result["id"], test_uid)
		with self.assertRaises(Exception):
			self.users_api.disable_user(-1)

	@patch('requests.delete')
	def test_delete_user(self, mock_delete_user):
		mock_delete_user.return_value.status_code = 204
		result = self.users_api.delete_user(0)
		self.assertEqual(result["status"], "Success")
		with self.assertRaises(Exception):
			self.users_api.delete_user()
		with self.assertRaises(Exception):
			self.users_api.delete_user("username")

	@patch('requests.post')
	def test_change_password(self, mock_change_password):
		mock_change_password.return_value.status_code = 204
		result = self.users_api.change_password(0, "test")
		self.assertEqual(result["status"], "Success")
		with self.assertRaises(Exception):
			self.users_api.change_password("1", "test")
		with self.assertRaises(Exception):
			self.users_api.change_password(1, None)

	@patch('requests.post')
	def test_regenerate_key(self, mock_regenerate_key):
		mock_regenerate_key.return_value.status_code = 200
		mock_regenerate_key.return_value.json.return_value = {
																"id": 0,
																"type": "local",
																"name": "string",
																"principal": "string",
																"isEnabled": True,
																"isSystem": True,
																"isAdmin": True,
																"isCurrent": True
															}
		mock_regenerate_key.return_value.headers = {"Content-Type": 'application/json;charset=utf-8'}
		result = self.users_api.regenerate_key(0)
		with self.assertRaises(Exception):
			self.users_api.regenerate_key("5")		

if __name__ == '__main__':
    unittest.main()