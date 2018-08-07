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


from CoSSH.Utils.FileWriting import InPlaceReplacement
from termcolor import colored
import os
import sys

class DeleteObject():

	def __init__(self):
		self.client_conf = "/etc/cossh/clients/clients.conf"

	def delete_group(self, groupname):
		group = self.catch_group(groupname)

		if not group:
			print(colored("Group '" + groupname + "' doesn't exist", "red"))
			sys.exit()

		public_key = "/etc/cossh/keys/cossh-key_" + groupname + ".pub"
		private_key = "/etc/cossh/keys/cossh-key_" + groupname

		InPlaceReplacement.remove_string_lines(group, self.client_conf)

		print(colored("Group '" + groupname + "' deleted", "green"))

		try:
			if os.path.exists(public_key):
				os.remove(public_key)

			if os.path.exists(private_key):
				os.remove(private_key)

			print(colored("Group keys removed", "green"))

		except PermissionError:
			print(colored("You are not permitted to deal with the keys", "red"))
			sys.exit()


	def remove_device(self, serial):
		check_string = InPlaceReplacement.search_string(self.client_conf, serial)

		if check_string == True:
			InPlaceReplacement.remove_string_line(serial, self.client_conf)
			print(colored("Device '" + str(serial) + "' removed from its host group", "green"))
		else:
			print(colored("Device '" + str(serial) + "' doesn't belong to any group", "yellow"))

	def catch_group(self, groupname):

		group_member = False
		group_members = []

		try:
			with open(self.client_conf) as cc:
				for line in cc:
					stripped_line = line.strip()
					if stripped_line == "@@" + groupname + "@@":
						group_member = True

					elif stripped_line.startswith("@@") or stripped_line == "":
						group_member = False

					if group_member == True:
						group_members.append(stripped_line)

				return group_members

		except FileNotFoundError:
			print(colored("/etc/cossh/clients/clients.conf doesn't exist", "red"))
			sys.exit()

		except PermissionError:
			print(colored("You are not permitted to deal with the groups", "red"))
			sys.exit()

		except Exception as e:
			print(colored(e, "red"))
