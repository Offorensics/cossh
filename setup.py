#!/usr/bin/env python3

import os
import sys
import shutil
import platform
import subprocess

check_root = os.geteuid()

# currently the program must be installed with priviledged permissions, but this is most likely going to change when the program is available
# to be installed with pip
if check_root != 0:
	print("Use 'sudo' to install this program. DO NOT install logged in as root, unless you are going to use the program as root.")
	sys.exit()

# check if a program is installed
# if not installed, check if distro is *ubuntu or debian
# if it is, try to install it
def check_installation(program):

	# pip3 is needed to install requirements
	if program == "pip3":
		apt_package = "python3-pip"

	# cossh uses setfacl command to change acl in /etc/cossh
	elif program == "setfacl":
		apt_package = "acl"

	elif program == "setuptools":
		apt_package = "python3-setuptools"

	release = platform.linux_distribution()

	# check if distro is *ubuntu or debian
	if shutil.which(program) == None:
		if any("buntu" in s for s in release) or "Debian" in release:
			cmd = "apt-get install -y " + apt_package
			os.system(cmd)
		else:
			print("Program " + program + " doesn't exist, please install it first and then run the setup.py again")
			sys.exit()

check_installation("pip3")
check_installation("setfacl")

try:
	from setuptools import setup
	from setuptools.command.install import install
except ImportError:
	check_installation("setuptools")

class UserInstall(install):
	def run(self):
		install.run(self)
		set_perms = 'bin/cossh-admin'
		os.system(set_perms)

setup(
        name='cossh',
        version='1.0.0',
        description='Router configuration automation/management tool',
        author='Joram Puumala',
        author_email='offorensics@gmail.com',
	license='MIT',
        packages=['CoSSH', 'CoSSH.GroupStatus', 'CoSSH.Configuration', 'CoSSH.Utils'],
	platforms=['Linux'],
	include_package_data=True,
        package_dir={'': 'lib'},
        url='https://github.com/Offorensics/cossh',
#        install_requires=[
#                        'paramiko==',
#                        'termcolor',
#                        'openpyxl',
#                        ],
        python_requires='>=3.4.*',
        data_files=[('/etc/cossh/clients', ['files/clients.txt']),
                    ('/etc/cossh/keys', ['files/keys.txt']),
                    ('/etc/cossh/configs', ['files/configs.txt'])],
        scripts=['bin/cossh',
		 'bin/cossh-admin',
	],
	cmdclass={'install': UserInstall},
        )
