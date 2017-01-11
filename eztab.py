#!/usr/bin/env python

import sys
import re
import os


class EasyTabCompletion(object):
	def __init__(self, raw_filename):
		self.TAB_HOSTILE_CHARS = '[. ,\-\&\(\)]'
		self.EXT_PTN = '\.[a-zA-Z0-9]{1,7}$'
		self.raw_filename = raw_filename
		self.processed_filename = ''
		self.ext = re.search(self.EXT_PTN, raw_filename)
		self.lameElements =  re.split(self.TAB_HOSTILE_CHARS, raw_filename)
		self.properElements = []
	
	def israw_filename(self):
		TAB_HOSTILE_CHARS_ptn = '\.(?![a-zA-Z0-9]{1,7}$)|\s'
		if re.search(TAB_HOSTILE_CHARS_ptn, self.raw_filename):
			return True
		return False

	def hasExt(self):
		if self.ext:
			self.ext = self.ext.group(0)
			return True
		else:
			return False

	def createprocessed_filename(self):
		if not self.israw_filename():
			self.processed_filename = (self.raw_filename[0].lower() + self.raw_filename[1:]) if (re.search('^[A-Z]', self.raw_filename)) else self.raw_filename
			return

		for i, element in enumerate(self.lameElements):
			if i == 0:
				self.properElements.append(element.lower())
				continue
			self.properElements.append(element.capitalize())
		if self.hasExt():
			del self.properElements[-1]
			self.properElements.append(self.ext)
		self.processed_filename = ''.join(self.properElements)
			
	def renameFile(self):
		if os.path.exists(os.path.abspath(self.raw_filename)):
			os.rename(os.path.abspath(self.raw_filename), self.processed_filename)
		else:
			print('No such file: ' + self.raw_filename)
			exit(1)



	def main():
		if len(sys.argv) == 1:
			print('Usage: {0} fileName'.format(sys.argv[0]))
			sys.exit(0)
		args = sys.argv[1:]
		for arg in args: 
			if os.path.exists(arg) and os.path.isfile(arg) or os.path.isdir(arg):
				prop_fn = EasyTabCompletion(os.path.basename(arg))
				prop_fn.createprocessed_filename()
				if prop_fn.raw_filename == prop_fn.processed_filename:
					continue
				prop_fn.renameFile()
				print('Renaming: \"{0}\" -> \"{1}\"'.format(prop_fn.raw_filename, prop_fn.processed_filename))
			else:
				print("No such file " + arg)
		return 0

if __name__ == '__main__':
	EasyTabCompletion.main()



