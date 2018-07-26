#!/usr/bin/env python3

import hashlib

class LocalHash():

	def calculate_md5(filepath):
		try:
			with open(filepath) as fp:
				file_data = fp.read()
				md5_sum = hashlib.md5(file_data.encode('utf-8')).hexdigest()

			return md5_sum

		except Exception as e:
			return e
