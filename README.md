# cossh

_Cossh_ is a simple configuration/configuration management tool written in Python(v3), specifically designed for [Advantech](http://advantech-bb.com/ "Advantech's") industrial routers. It is inspired by _Ansible_, which configures endpoints over SSH connections (no need for an agent). _Cossh_ does the same, it configures endpoints over SSH connections. _Cossh_ reads a _cossh file_ which (currently) uses its own _cossh syntax_ to determine a configuration to be sent to endpoints. Writing a cossh/configuration file is straightforward and fast, and it ships with functions that are designed to do common tasks that administrators would otherwise do using devices' web GUI. _Cossh_ can be used to automate pre-configuriation of routers and manage configured routers which belong to groups.

# What about SmartWorxHub?

_SmartWorxHub_ is Advantech-BB's configuration management tool for the company's industrial routers, and Cossh is not aiming to replace it. Cossh is a free open-source tool that can manage routers just like SmartWorxHub. It was created to complement SmartWorxHub's shortcomings. Note that SmartWorxHub provides some useful features that Cossh doesn't (yet, check what is next part!). When choosing which configuration management tool to use and in which case, you should at least ask yourself the following questions: How big is my network of routers? Do I need an agent that connects from routers to SmartWorxHub? Do the routers have a management IP (e.g. VPN)? How widely are the routers distributed? 

# Cossh syntax and general rules

Cossh has its own syntax for reading a cossh/configuration file. The correct syntax is to give a command at the beginning of a line, followed by an equal sign (=) and required parameters. Note that the equal sign MUST have one whitespace on both sides, separating it from the command and the required parameters. Currently, required parameters need to be in a specific order. An example configuration file will help with the syntax, after which it is easy to learn. Each required parameter must be separated by comma (,).

**Incorrect Syntax**
```
add-um= /home/offorensics/mymodule.tgz      #no whitespace on both sides of the equal (=) sign
create-user = cossh password123 admin       #no commas used to separate required parameters
change-passwd=cossh,n3wpassword-!           #no whitespaces used at all around the equal (=) sign
```

**Correct Syntax**
```
add-um = /home/offorensics/mymodule.tgz
create-user = cossh, password123, admin
change-passwd = cossh,n3wpassword-!
```

Cossh reads a given cossh file from top to bottom, so that is the order functions will be called. Because of this, get to know how Cossh functions operate, to avoid unexpected results. For example when configuring multiple profiles, most recently configured profile will be an active profile after a reboot.

# /etc/cossh

Configuration files are currently stored in **/etc/cossh** (only cossh file can be anywhere).

**/etc/cossh/clients** - _client.conf_ file is stored here. The file contains configuration groups and their clients. The file should NOT be edited manually.

**/etc/cossh/configs** - Unique configuration files are stored here. Unique configuration files use the following naming syntax; `cossh_<router_serial>.cfg`.

**/etc/cossh/keys** - Groups' SSH keys are stored here. 

# Installation

Currently Cossh can only be installed from the source, but future versions will be available via pip.

**1.**
 
Download the latest Cossh tarball <here>

**2.**

Extract the tarball with the command below (change version numbering if needed).

```
tar -xzvf cossh_1.0.0.tar.gz
```

**3.**

Change directory to `cossh_<version>` and run _setup.py_ script with sudo.

```
cd cossh_1.0.0
sudo ./setup.py install
```

**4.**

Install requirements.

```
pip3 install -r requirements.txt
```

You are ready to go!

# Giving another user on the same system permission to run cossh (not recommended)

It is not recommended to have multiple users on the same system to run cossh, but it is possible. Follow the instructions below to setup a new user.

**1.**

Run cossh-admin as root, and give that new user as a parameter

```
cossh-admin <user>
```

**2. (may be required)**

If you didn't install requirements earlier globally (installing globally is not usually wise), you have to install the same requirements again for the new user. Login as the new user and use the same requirements file you used earlier.

```
pip3 install -r requirements.txt
```

# Supported router models

```
SmartMotion (*)
SmartStart (*)
SmartFlex (*)
UR5 (*)
ER75 (*)
LR77 (*)

(*) - This model and its submodels
```

Other routers by Advantech should work as well, but the models listed above have been tested.


# Operating System requirements

A Linux operating system is required. Debian based distribution is recommended.

# Cossh optional arguments

**-h**, **--help**

Shows help message and exits

**-f [COSSH CFG FILE]**

Requires one argument, path to cossh configuration file. This allows instructions to be read from a file by any name or accessible location.

**-c [ROUTER CFG FILE]**

Requires one argument, path to router's configuration file. Router's configuration file contains router settings. Note that if **-c** argument is used, this is the first action cossh does after loggin in. This argument doesn't work with group configuration.

**-s**

Suppresses normal output

**-o [GROUP]**

Gets online status of a group and exits.

**--groups**

Lists all existing client groups and exits.

**--example**

Generates example cossh configuration file. The file includes all supported commands and their correct syntax, and one example for each command.

**--del-group [GROUP]**

Deletes given group and exits.

**--del-device [DEVICE SERIAL]**

Deletes given device from its group

# Cossh functions

### add-client

Adds a router/client to a given group. Requires **router's management IPv4 address** and **group name**. Management IPv4 address is the address through which cossh will later connect to router to change configuration or fetch data. In many cases this management address is a VPN address, but can be any. The idea is that every router in the same group can be accessed from the same network. Note that each group can only contain unique IPv4 addresses, but two groups may share the same IPv4 addresses. One device can be in one group at a time. This function is not available when logged into a router with SSH key.

Example below adds router with IPv4 address _10.100.194.1_ to group cossh.

```
SYNTAX
add-client = <management_IPv4_address>, <group>

EXAMPLE
add-client = 10.100.194.1, cossh
```

### add-um

Installs a user module to router. Requires **a path to user module**. One user module can be specified in one call.

Example below installs user module _mymodule.tgz_ in router.

```
SYNTAX
add-um = <path_to_user_module>

EXAMPLE
add-um = /home/offorensics/mymodule.tgz
```

### change-passwd

Changes given user's password. Requires **<username>** and **<password>**. Old password is not needed. Has two available variables **($serial)** and **($mac)** which can be used anywhere in password. **($serial)** will be replaced with router's serial number and **($mac)** with router's primary MAC address.

Example below changes user _offorensics_'s password to _w3akone345!_.

```
VARIABLES
($serial)
($mac)

SYNTAX
change-passwd = <username>, <password>

EXAMPLE
change-passwd = offorensics, w3akone345!
```

### create-user

Creates new user in router. The user can be regular user or administrator. Requires three values, **<username>**, **<password>** and **regular/admin**. Has two available variables **($serial)** and **($mac)** which can be used anywhere in new user's password. **($serial)** will be replaced with router's serial number and **($mac)** with router's primary MAC address.

Example below creates a regular user called _slave_, sets user's password to _An0therW3ak10!_.

```
VARIABLES
($mac)
($serial)

SYNTAX
create-user = <username>, <password>, regular/admin

EXAMPLE
create-user = slave, An0therW3ak10!, regular
```

### delete-user

Deletes given user from router. Requires only **<username>**.

Example below deletes user _slave_ from router.

```
SYNTAX
delete-user = <username>

EXAMPLE
delete-user = slave
```

### latest-update

Fetches the latest update/configuration information from router and prints it out to standard output. See **update-name** function for more information about the latest update feature.

Example below fetches the latest update from router.

```
SYNTAX
latest-update = show

EXAMPLE
latest-update = show
```

### login

Logs into router with password. The program requires _root_ login, so only **IPv4 address** and **password** need to be provided.

Example below logs into a router at _192.168.10.1_.

```
SYNTAX
login = <IPv4_address>, <password>

EXAMPLE
login = 192.168.10.1, toor
``` 

### login-group

Logs into routers with encrypted SSH key (group's key). **Group name** needs to be provided. Will attempt to log into every single router in the group.

Example below logs into routers belonging to group _cossh_.

```
SYNTAX
login-group = <group_name>

EXAMPLE
login-group = cossh
``` 

### login-key

Logs into router with encrypted SSH key (client's group's key). **IPv4 address** and **group name** must be provided.

Example below logs into a router at _192.168.10.1_.

```
SYNTAX
login-key = <IPv4_address>, <group_name>

EXAMPLE
login-key = 192.168.10.1, cossh
```

### router-command

Runs a given command in router. Warning, the function waits for the command to finish, so you might consider adding an ampersand **(&)** at the end of your command when starting some services. This will run the command in the background and make the function return.

```
SYNTAX
router-command = <custom command>

EXAMPLE
router-command = /etc/init.d/eth restart
```

### reboot

Reboots router. Not recommended to be used in the middle of configuration, because the command will end it.

Example below shows how to reboot a router

```
SYNTAX
reboot

EXAMPLE
reboot
```

### remove-um

Removes a given user module from router. Requires **name of the user module**. User module name is user module's root directory's name.

Example below removes user module _mymodule.tgz_ from a router.

```
SYNTAX
remove-um = <user_module_name>

EXAMPLE
remove-um = mymodule
```

### save-unique

Imports router's current configuration and saves it under **/etc/cossh/configs/** as the router's unique configuration file.

```
SYNTAX
save-unique = true

EXAMPLE
save-unique = true
```

### sws

Configures a single parameter in router (currently only standard profile). Requires **setting/value pair**. Notice that it is extremely important to have no whitespaces around the equal (=) sign between **setting** and **value** in **setting/value pair** (don't confuse this with cossh syntax)! Two variables are available, **$serial** and **$mac** which can be used to replace value in **setting/value pair**. **$serial** will be replaced with router's serial number and **$mac** with router's primary MAC address.

Examples below set parameter SNMP\_NAME to router's serial number and ETH\_IPADDR to _192.168.50.1_.

```
VARIABLES
$mac
$serial

SYNTAX
sws = <settings>=<value>

EXAMPLES
sws = SNMP_NAME=$serial
sws = ETH_IPADDR=192.168.50.1
```

### update-name

Stores a custom update message in router. Only works when a change in configuration is made in router, otherwise the latest update message remains intact. By default (if function is not used), update message will be **Update - DATE TIME**. Note that date and time will be automatically concatenated to your custom string.

Example below creates custom update message.

```
SYNTAX
update-name = <custom message>

EXAMPLE
update-name = Firmware updated to version 6.1.5
```

### upload-cfg

Configures router settings with a configuration file. Requires **a path to configuration file** and **profile (standard/alt1/alt2/alt3)**. A path to configuration file can be replaced with variable **$unique**, which can come handy with group configuration when there are device specific configuration values such as certificates. When used, cossh looks for clients' unique configuration files in **/etc/cossh/configs/** and use the files as the clients' configuration files. Unique configuration files use special naming syntax, which is `cossh_<router_serial>.cfg`. The configuration will be saved in selected profile. **NOTE:** The most recently configured profile will be active after rebooting router.

Example below uploads a router configuration file _mytestconf.cfg_ to **standard** profile.

```
VARIABLES
$unique

SYNTAX
upload-cfg = <path_to_configuration_file>, standard/alt1/alt2/alt3

EXAMPLE
upload-cfg = /home/offorensics/mytestconf.cfg, standard
```
 
### upload-file

Uploads a file to router. You can upload any file to router (as long as there is space left), for example a shell script or iptables rules that you have made. Function requires **a path to local file** and **remote directory (in router)**. **Remote directory** is the directory where the file will be sent to.

Example belows uploads shell script _counter.sh_ to **/root** directory.

```
SYNTAX
upload-file = <path_to_local_file>, <remote_location>

EXAMPLE
upload-file = /home/offorensics/counter.sh, /root
```

### write-excel

Writes a custom value to given **.xlsx** file. Requires **a value**, **a path to .xlsx file**, **sheetname** and **column**. Currently three variables are available, **$serial**, **$mac** and **$date**, which can be used as custom values. **$serial** will be replaced with router's serial number and **$mac** with router's primary MAC address. **$date** will be replaced with current date. **NOTE:** the value will be written to the first empty cell under a given column.

Example below writes router's MAC address to column **A** and string **This device is OK** to column **D**, on sheet **Routers** in **delivered_routers.xlsx**.

```
VARIABLES
$date
$mac
$serial

SYNTAX
write-excel = <custom value>, <path_to_xlsx_file>, <sheetname>, <column>

EXAMPLES
write-excel = $mac, /home/offorensics/delivered_routers.xlsx, Routers, A
write-excel = This device is OK, /home/offorensics/delivered_routers.xlsx, Routers, D
```

# What is next?

There are lots of areas of improvement, which will be addressed sooner or later. Below I listed a few important ones.

**Code**

There's still some repetition in the program's code, and unnecessary commands that don't need to be there (e.g. bash commands). Most of such commands will be replaced with pure Python solutions.

**Installation**

Currently Cossh has to be built from source, but eventually it will be available via **pip** (.whl).

**Features**

Cossh lacks some features that will be added in future versions, probably the most important will be firmware upgrade, which is coming soon (possible now as well but needs custom commands). Few of the current features also need revamping.

**Alternative configuration method**

As router's API evolves, it will be possible to choose between configuration over SSH and API. This will happen at some point, but currently the API doesn't support all needed functions. 

**Router State**

There will be more statistics available, such as router's temperature and signal strength, and much more.

# Bugs and issues

See known bugs and issues [bugs and issues](https://github.com/Offorensics/cossh/issues "here").

# License

Cossh is released under the [MIT License](https://opensource.org/licenses/MIT "MIT License")
