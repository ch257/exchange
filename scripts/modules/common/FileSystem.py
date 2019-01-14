# -*- coding: utf-8 -*


class FileSystem:
	def __init__(self, errors):
		self.errors = errors
	
	def create_folder_branch(self, path):
		path = path.replace('\\', '/')
		folders = path.split('/')
		for folder in folders:
			if folder:
				print(folder)
