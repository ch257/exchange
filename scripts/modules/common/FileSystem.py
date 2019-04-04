# -*- coding: utf-8 -*

import os

class FileSystem:
	def __init__(self, errors):
		self.errors = errors
	
	def create_folder_branch(self, path):
		if self.errors.error_occured:
			return None

		path = path.replace('\\', '/')
		folders = path.split('/')
		folder_path = ''
		for folder in folders:
			if folder:
				folder_path += folder + '/'
				if not os.path.exists(folder_path):
					try:
						os.makedirs(folder_path)
					except Exception as e:
						self.errors.raise_error('Can\'t create folder' + folder_path)
						break
		return None
		
	def split_file_path(self, path):
		if self.errors.error_occured:
			return None
		
		path = path.replace('\\', '/')
		folders = path.split('/')
		file_name = folders.pop(len(folders) - 1)
		folder_path = ''
		for folder in folders:
			if folder:
				folder_path += folder + '/'
		
		return folder_path, file_name
		
	def get_folder_list(self, folder):
		lst = []
		try:
			lst = os.listdir(folder)
		except Exception as e:
			self.errors.raise_error('Can\'t open folder' + folder)
		
		return lst