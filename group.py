class Group:
	def __init__(self, name):
		self.name = name
		self.users = []

	def add_user(self, user):
		self.users.append(user)


	def get_name(self):
		return self.name


	def get_users(self):
		return self.users