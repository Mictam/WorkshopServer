
class Settings():
	def __init__(self, robot_language, voice, volume, app_language):
		self.robot_language = robot_language
		self.voice = voice
		self.volume = volume
		self.app_language = app_language

	def change_settings(self, robot_language, voice, volume, app_language):
		self.robot_language = robot_language
		self.voice = voice
		self.volume = volume
		self.app_language = app_language

	def send_settings_to_robot(self):
		return True