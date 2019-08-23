from apiclient.apiclient import APIClient
import json
import re

# Projects Client for Code DX Projects API
class Users(APIClient):
	
	def __init__(self, base, api_key, verbose = False):
		""" Creates an API Client for Code DX Users API
				base: String representing base url from Code DX
				api_key: String representing API key from Code DX
				verbose: Boolean - not supported yet

		"""
		super().__init__(base, api_key, verbose)
		self.user_types = {'Local': 'local', 'LDAP': 'ldap', 'External': 'external', 'Key': 'key', 'All': ''}

	def create_user(self, name, pw, enabled, user_type):
		""" Creates a user based on given user type.
		"""
		local_url = '/api/admin/users/%s' % self.user_types[user_type]
		self.type_check(name, str, "Username")
		self.type_check(pw, str, "Password")
		self.type_check(enabled, bool, "Enabled")
		user = {'name': name, 'password': password, 'enabled': enabled}
		params = {'user': user}
		res = self.call("POST", local_path=local_url, json=params)
		return res

	def get_all_users(self, user_type):
		local_url = '/api/admin/users/%s' % self.user_types[user_type]
		res = self.call("GET", local_path=local_url)
		return res

	def get_users(self):
		""" Returns a list of all users.
		"""
		return get_all_users(self, 'All')

	def create_local(self, name, pw, enabled):
		""" Creates a local user.
		"""
		return create_user(self, name, pw, enabled, 'Local')

	def get_locals(self):
		""" Gets local users.
		"""
		return get_all_users(self, 'Local')

	def create_ldap(self, name, pw, enabled):
		""" Creates a ldap user.
		"""
		return create_user(self, name, pw, enabled, 'LDAP')

	def get_ldaps(self):
		""" Gets ldap users.
		"""
		return get_all_users(self, 'LDAP')

	def create_external(self, name, pw, enabled):
		""" Creates an external user.
		"""
		return create_user(self, name, pw, enabled, 'External')

	def get_externals(self):
		""" Gets external users.
		"""
		return get_all_users(self, 'External')

	def create_key(self, name, pw, enabled):
		""" Creates an api key.
		"""
		return create_user(self, name, pw, enabled, 'Key')

	def get_keys(self):
		""" Gets api keys.
		"""
		return get_all_users(self, 'Key')

	def user_settings(self, uid, isEnabled, isAdmin):
		self.type_check(isEnabled, bool, "isEnabled")
		self.type_check(isAdmin, bool, "isAdmin")
		self.type_check(uid, int, "User ID")
		local_url = '/api/admin/users/%d' % uid
		user_settings = {"isEnabled": isEnabled, "isAdmin": isAdmin}
		params = {'disableUser': user_settings}
		res = self.call("PUT", local_path=local_url, json=params)
		return res

	def delete_user(self, uid):
		""" To delete a user, you must know its id (found from its corresponding user object).
		"""
		self.type_check(uid, int, "User ID")
		local_url = '/api/admin/users/%d' % uid
		res = self.call("GET", local_path=local_url)
		return res

	def change_password(self, uid, pw):
		self.type_check(uid, int, "User ID")
		self.type_check(pw, str, "New Password")
		params = {"password": pw}
		local_path = "/api/admin/users/local/%d/password" % uid
		res = self.call("POST", local_path=local_url, json=params)
		return res

	def regenerate_key(self, uid):
		self.type_check(uid, int, "User ID")
		local_path = "/api/admin/users/key/%d/regenerate" % uid
		res = self.call("POST", local_path=local_url)
		return res