#!/usr/bin/env python3

import os
import sys
import shutil
import platform
import subprocess

check_root = os.geteuid()

def check_installation(program):
	if program == "pip3":
		apt_package = "python3-pip"
	elif program == "setfacl":
		apt_package = "acl"
	elif program == "setuptools":
		apt_package = "python3-setuptools"

	release = platform.linux_distribution()

	if shutil.which(program) == None:
		if any("buntu" in s for s in release) or "Debian" in release:
			cmd = "apt-get install -y " + apt_package
			subprocess.call([cmd], shell=True)
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

if check_root != 0:
    print("Use 'sudo' to install this program")
    sys.exit()

class UserInstall(install):
    def run(self):
        install.run(self)
        set_perms = 'bin/cossh-admin'
        install_requirements = 'pip3 install -r requirements.txt'
        os.system(set_perms)
        os.system(install_requirements)

setup(
        name='cossh',
        version='1.0.0',
        description='Router configuration management tool',
        author='Joram Puumala',
        author_email='offorensics@gmail.com',
        packages=['CoSSH', 'CoSSH.GroupStatus', 'CoSSH.Configuration', 'CoSSH.Utils'],
	include_package_data=True,
        package_dir={'': 'lib'},
        url='http://offorensics.com',
        install_requires=[
                        'paramiko==2.3.1',
                        'termcolor',
                        'openpyxl',
                        ],
        python_requires='>=3.4.*',
        data_files=[('/etc/cossh/clients', ['files/clients.txt']),
                    ('/etc/cossh/keys', ['files/keys.txt']),
                    ('/etc/cossh/configs', ['files/configs.txt'])],
        scripts=['bin/cossh',
		 'bin/cossh-admin',
	],
	cmdclass={'install': UserInstall},
        )
