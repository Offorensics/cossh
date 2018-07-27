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


import subprocess
from termcolor import colored
from multiprocessing import Pool, TimeoutError

class CosshStatus():
	def __init__(self):
		self.client_file = "/etc/cossh/clients/clients.conf"

	# function to get online hosts from a group
	def get_online(self, clientgroup):

		client_list = []
		client_bool = False

		try:
			# read clients.conf file
			with open(self.client_file) as cc:
				for line in cc:

					# try to search for a given group in clients.conf
					if line.strip().startswith("@@") and line.strip().endswith("@@"):
						if line.strip() == "@@" + clientgroup + "@@":
							client_bool = True
						else:
							client_bool = False

					# if group exists, append group's clients' IPv4 addresses to client_list
					if client_bool == True and not line.strip().startswith("@@") and line.strip() != "":
						client_ip = line.strip().split(":", 1)[0]
						client_list.append(client_ip)

			try:
				# call ping_processes function and start each as its own process
				ping_processes = Pool(processes=len(client_list))
				data = ping_processes.map_async(self.ping_client, [client_list[i] for i in range(len(client_list))])
				ping_processes.close()
				ping_processes.join()

			except TimeoutError:
				print(colored("error", "red"))

			except ValueError:
				print(colored("No clients in group '" + clientgroup + "'", "red"))

			except Exception as e:
				print(colored(e, "red"))

		except FileNotFoundError:
			print(colored("No groups found (client.conf doesn't exist)", "red"))

		except Exception as e:
			print(colored(e, "red"))

	# function to ping a given IPv4 address
	def ping_client(self, host):
		cmd = "timeout 2 ping -c 1 " + host + " 2>&1 >/dev/null ;echo $?"
		online_status = subprocess.check_output([cmd], shell=True).decode('utf-8').strip()

		if online_status == "0":
			print(host + ":" + colored(" Online", "green"))
		else:
			print(host + ":" + colored(" Offline", "red"))

	# fetches existing client groups
	def get_groups(self):
		group_count = 0

		try:
			with open(self.client_file) as clients:
				for client in clients:
					if client.startswith("@@"):
						group_count += 1
						print(client.replace("@@", "").strip())

			if group_count == 0:
				print(colored("No groups found", "red"))
			else:
				print("\nNumber of groups: " + colored(str(group_count), "yellow"))

		except FileNotFoundError:
			print(colored("No groups found (client.conf doesn't exist)", "red"))

		except PermissionError:
			print(colored("Invalid file permissions for '" + self.client_file + "'", "red"))

		except Exception as e:
			print(e)


	def generate_cfg(self):
		example_file = "cossh_example.cfg"

		try:
			with open(example_file, "w") as ef:
				ef.write("# Example cossh configuration file containing syntax of every available command\n\n")
				ef.write("# add-client = <client_ipv4_address>, <group>\nadd-client = 10.100.194.1, cossh_group\n\n")
				ef.write("# add-um = <path_to_user_module>\nadd-um = /home/cossh/user_modules/mymodule.tgz\n\n")
				ef.write("# change-passwd = <user_name>, <password>\nchange-passwd = cossh_user, MynewP455!?\n\n")
				ef.write("# create-user = <user_name>, <password>, admin/regular\ncreate-user = cossh_user, B1gsecret10-!, admin\n\n")
				ef.write("# delete-user = <user_name>\ndelete-user = cossh_user\n\n")
				ef.write("# latest-update = show\nlatest-update = show\n\n")
				ef.write("# login = <IPv4 address>, <password>\nlogin = 192.168.1.1, toor\n\n")
				ef.write("# login-group = <group>\nlogin-group = cossh_group\n\n")
				ef.write("# login-key = <IPv4 address>, <group>\nlogin-key = 192.168.1.1, cossh_group\n\n")
				ef.write("# reboot\nreboot\n\n")
				ef.write("# remove-um = <user_module_name>\nremove-um = mymodule\n\n")
				ef.write("# router-command = <custom command>\nrouter-command = /etc/init.d/eth restart\n\n")
				ef.write("# sws = <setting_value_pair>\nsws = SNMP_NAME=example_name\n\n")
				ef.write("# update-name = <custom update message>\nupdate-name = Updated firmware to 6.1.5\n\n")
				ef.write("# upload-cfg = <path_to_cfg_file>, standard/alt1/alt2/alt3\nupload-cfg = /home/cossh/configs/router_settings.cfg, standard\n\n")
				ef.write("# upload-file = <path_to_local_file>, <path_to_remote_location>\n\nupload-file = /home/cossh/files/example_file.txt, /root\n\n")
				ef.write("# write-excel = <custom_value>, <path_to_excel_file>, <sheet_name>, <column>\nwrite-excel = $serial, /home/cossh/data/routers.xlsx, routers, B\n")

			print("Created " + example_file)

		except PermissionError:
			print(colored("Permission denied, can't create an example file in this directory", "red"))

		except Exception as e:
			print(colored(e, "red"))
