#!/usr/bin/env python3

#Copyright (c) 2018 Joram Puumala
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


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

	def search_string(cfg_file, string):
		try:
			with open(cfg_file) as cf:
				if string in cf.read():
					return True
				else:
					return False
		except PermissionError:
			print("Invalid file permissions for '" + filename + "'")

		except Exception as e:
			print(e)

