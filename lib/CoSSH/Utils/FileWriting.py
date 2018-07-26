#!/usr/bin/env python3

import os
import tempfile

class InPlaceReplacement():

	# replaces matching strings with given strings
	def replace_string(old, new, filename):

		try:
			with tempfile.NamedTemporaryFile('w', delete=False) as outfile:
				with open(filename) as infile:
					for line in infile:
						if old in line:
							line = line.replace(old, new)
						outfile.write(line)

			os.replace(outfile.name, filename)

		except FileNotFoundError:
			print(filename + ", no such file or directory")

		except PermissionError:
			print("Invalid file permissions for '" + filename + "'")

		except Exception as e:
			print(e)

	# writes a given string after matching strings
	def after_string(match, string, filename):

		try:
			with tempfile.NamedTemporaryFile('w', delete=False) as outfile:
				with open(filename) as infile:
					for line in infile:
						outfile.write(line)
						if match in line:
							outfile.write(string + "\n")

			os.replace(outfile.name, filename)

		except FileNotFoundError:
			print(filename + ", no such file or directory")

		except PermissionError:
			 print("Invalid file permissions for '" + filename + "'")

		except Exception as e:
			print(e)

	# removes lines where matching strings are found
	def remove_string_line(string_line, filename):

		try:
			with tempfile.NamedTemporaryFile('w', delete=False) as outfile:
				with open(filename) as infile:
					for line in infile:
						if not string_line in line:
							outfile.write(line)

			os.replace(outfile.name, filename)

		except FileNotFoundError:
			print(filename + ", no such file or directory")

		except PermissionError:
			 print("Invalid file permissions for '" + filename + "'")

		except Exception as e:
			print(e)
