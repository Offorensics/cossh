# What is cossh?

_Cossh_ is a simple configuration/configuration management tool written in Python(v3), specifically crafted for [Advantech](http://advantech-bb.com/ "Advantech's") industrial routers. It is inspired by _Ansible_, which configures endpoints over SSH connections (no need for an agent). _Cossh_ does the same, it configures endpoints over SSH connections. _Cossh_ reads a _cossh file_ which (currently) uses its own _cossh syntax_ to determine a configuration to be sent to endpoints. Writing a cossh/configuration file is straightforward and fast, and it ships with functions that are designed to do common tasks that administrators would otherwise do using devices' web GUI. _Cossh_ can be used to pre-configure routers and manage configured routers which belong to groups.

# What about SmartWorxHub?

_SmartWorxHub_ is _Advantech-BB's_ configuration management tool for the company's industrial routers, and _Cossh_ is not aiming to replace it. _Cossh_ is a free open-source tool that can manage routers just like _SmartWorxHub_. It was created to complement _SmartWorxHub's_ shortcomings. Note that _SmartWorxHub_ provides some useful features that _Cossh_ doesn't (yet). When choosing which configuration management tool to use and in which case, you should at least ask yourself the following questions: How big is my network of routers? Do I need an agent that connects from routers to _SmartWorxHub_? Do the routers have a management IP (e.g. VPN)? How widely are the routers distributed? 

# Cossh syntax and general rules

_Cossh_ has its own syntax for reading of a cossh/configuration file. The correct syntax is to give a command at the beginning of a line, followed by an equal sign (=) and required parameters. Note that the equal sign MUST have one whitespace on both sides, separating it from the command and the required parameters. Currently, required parameters need to be in a specific order, but an example configuration file will help with the syntax after which they are easy to learn. Each required parameter must be separated by comma (,).

**Incorrect Syntax**
```
add-um= /home/offorensics/mymodule.tgz
create-user = cossh password123 admin
change-passwd=cossh,n3wpassword-!
```

**Correct Syntax**
```
add-um = /home/offorensics/mymodule.tgz
create-user = cossh, password123, admin
change-passwd = cossh,n3wpassword-!
```

_Cossh_ reads a given cossh file from top to bottom, so that is the order functions will be called. Because of this, get to know how _Cossh_ functions operate, to avoid unexpected results. For example when configuring multiple profiles, most recently configured profile will be an active profile after a reboot.

# /etc/cossh

Configuration files are currently stored in _/etc/cossh_ (only cossh file can be anywhere).

**/etc/cossh/clients** - _client.conf_ file is stored here. The file contains configuration groups and their clients.

**/etc/cossh/configs** - Unique configuration files are stored here. Unique configuration files use the following syntax; _cossh\_<router\_serial>.cfg_.

**/etc/cossh/keys** - Groups' SSH keys are stored here. 

# Installation

Currently _Cossh_ can only be installed from the source, but future versions will be available via pip.

**1.**
 
Install the latest _Cossh_ tarball <here>

**2.**

Extract the tarball with the command below (change version numbering if needed).

```
tar -xzvf cossh_1.0.0.tar.gz
```

**3.**

Run _setup.py_ script with sudo.

```
sudo ./setup.py install
```

**4.**

Install requirements.

```
pip3 -r requirements.txt
```

That's it. You are ready to go.

# Supported routers

SmartMotion (\*)
SmartStart (\*)
SmartFlex (\*)
UR5 (\*)
ER75 (\*)
LR77 (\*)


(\*) - _This model and its submodels_

# Operating System requirements

A Linux operating system is required. Debian based distribution is recommended.

# Cossh optional arguments

**-h**, **--help**

Shows help message and exits

**-f [COSSH CFG FILE]**

Requires one argument, path to cossh configuration file. This allows instructions to be read from a file by any name or accessible location.

**-c [ROUTER CFG FILE]**

Requires one argument, path to router's configuration file. Router's configuration file contains router settings. Note that if **-c** argument is used, this is the first action _cossh_ does after loggin in. This argument doesn't work with group configuration.

**-s**

Suppresses normal output

**-o [GROUP]**

Gets online status of a group and exits.

**--groups**

Lists all existing client groups and exits.

**--example**

Generates example cossh configuration file. The file includes all supported commands and their correct syntax, and one example for each command.

# Cossh functions

**add-client**

Adds a router/client to a given group. Requires _router's management IPv4 address_ and _group name_. Management IPv4 address is the address through which _cossh_ will later connect to router to change configuration or fetch data. In many cases this management address is a VPN address, but can be any. The idea is that every router in the same group can be accessed from the same network. Note that each group can only contain unique IPv4 addresses, but two groups may share the same IPv4 addresses. One device can be in one group at a time. This function is not available when logged into a router with SSH key.

Example below adds router _10.100.194.1_ to group cossh.

```
SYNTAX
add-client = <management_IPv4_address>, <group>

EXAMPLE
add-client = 10.100.194.1, cossh
```

**add-um**

Installs user module to router. Requires _a path to user module_. One user module can be specified in one call.

Example below installs user module _mymodule.tgz_ in router.

```
SYNTAX
add-um = <path_to_user_module>

EXAMPLE
add-um = /home/offorensics/mymodule.tgz
```

**change-passwd**

Changes given user's password. Requires _<username>_ and _<password>_. Old password is not needed. Has two available variables ($serial) and ($mac) which can be used anywhere in password. ($serial) will be replaced with router's serial number and ($mac) with router's primary MAC address.

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

**create-user**

Creates new user in router. The user can be regular user or administrator. Requires three values, _username_, _password_ and _regular/admin_. Has two available variables ($serial) and ($mac) which can be used anywhere in new user's password. ($serial) will be replaced with router's serial number and ($mac) with router's primary MAC address.

Example below creates a regular user called _slave_, sets user's password as _An0therW3ak10!_.

```
VARIABLES
($mac)
($serial)

SYNTAX
create-user = <username>, <password>, regular/admin

EXAMPLE
create-user = slave, An0therW3ak10!, regular
```

**delete-user**

Deletes given user from router. Requires only _username_.

Example below deletes user _slave_ from a router.

```
SYNTAX
delete-user = <username>

EXAMPLE
delete-user = slave
```

**latest-update**

Fetches the latest update/configuration information from router and prints it out to standard output. See _update-name_ function for more information about the latest update feature.

Example below fetches the latest update from a router.

```
SYNTAX
latest-update = show

EXAMPLE
latest-update = show
```

**login**

Logs into router with password. The program requires _root_ login, so only _IPv4 address_ and _password_ need to be provided.

Example below logs into a router at _192.168.10.1_.

```
SYNTAX
login = <IPv4_address>, <password>

EXAMPLE
login = 192.168.10.1, toor
``` 

**login-group**

Logs into routers with encrypted SSH key (group's key). _Group name_ needs to be provided. Will attempt to log into every single router in the group.

Example below logs into routers belonging to group _cossh_.

```
SYNTAX
login-group = <group_name>

EXAMPLE
login-group = cossh
``` 

**login-key**

Logs into router with encrypted SSH key (client's group's key). _IPv4 address_ and _group name_ must be provided.

Example below logs into a router at _192.168.10.1_.

```
SYNTAX
login-key = <IPv4_address>, <group_name>

EXAMPLE
login-key = 192.168.10.1, cossh
```

**router-command**

Runs a given command in router. Warning, the function waits for the command to finish, so you might consider adding an ampersand (&) at the end of your command when starting some services. This will run the command in background and make the function return.

```
SYNTAX
router-command = <custom command>

EXAMPLE
router-command = /etc/init.d/eth restart
```

**reboot**

Reboots router. Not recommended to be used in the middle of configuration, because the command will end it.

Example below shows how to reboot a router

```
SYNTAX
reboot

EXAMPLE
reboot
```

**remove-um**

Removes a given user module from router. Requires _name of the user module_. User module name is user module's root directory's name.

Example below removes user module _mymodule.tgz_ from a router.

```
SYNTAX
remove-um = <user_module_name>

EXAMPLE
remove-um = mymodule
```

**sws**

Configures a single parameter in router (currently standard profile). Requires setting/value pair. Notice that it is extremely important to have no whitespaces around the equal (=) sign between _setting_ and _value_ in setting/value pair! Two variables are available, _$serial_ and _$mac_ which can be used to replace value in setting/value pair. _$serial_ will be replaced with router's serial number and _$mac_ with router's primary MAC address.

Examples below set parameter _SNMP_NAME_ to router's serial number and _ETH_IPADDR_ to _192.168.50.1_.

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

**update-name**

Stores a custom update message in router. Only works when a change is made in a router, otherwise the latest update message remains intact. By default (if function is not used), update message will be _Update - DATE TIME_. Note that date and time will be automatically concatenated to your custom string.

Example below creates custom update message.

```
SYNTAX
update-name = <custom message>

EXAMPLE
update-name = Firmware updated to version 6.1.5
```

**upload-cfg**

Configures router settings with a configuration file. Requires _a path to configuration file_ and _profile_. _A path to configuration file can be replaced with variable _$unique_, which can come handy with group configuration when there are device specific configuration values such as certificates. When used, _cossh_ looks for client's unique configuration file in _/etc/cossh/configs/_ and uses it as the client's configuration file. Unique configuration files use special naming syntax, which is _cossh\_<router_serial>.cfg_. The configuration will be saved in selected profile. The most recently configured profile will be active after rebooting router.

Example below uploads a router configuration file _mytestconf.cfg_ to _standard_ profile.

```
VARIABLES
$unique

SYNTAX
upload-cfg = <path_to_configuration_file>, standard/alt1/alt2/alt3

EXAMPLE
upload-cfg = /home/offorensics/mytestconf.cfg, standard
```
 
**upload-file**

Uploads a file to router. You can upload any file to router (as long as there is space left), for example a shell script or iptables rules that you have made. Function requires _a path to local file_ and _a destination in remote destination_. _Remote destination_ is the directory where the file will be sent to.

Example belows uploads shell script _counter.sh_ to _/root_ directory.

```
SYNTAX
upload-file = <path_to_local_file>, <remote_location>

EXAMPLE
upload-file = /home/offorensics/counter.sh, /root
```

**write-excel**

Writes a custom value to given _.xlsx_ file. Requires _a value_, _a path to .xlsx file_, _sheetname_ and _column_. Currently three variables are available, _$serial_, _$mac_ and _$date_, which can be used as custom values. _$serial_ will be replaced with router's serial number and _$mac_ with router's primary MAC address. _$date_ will be replaced with current date. Note that the value will be written to the first empty cell under a column.

Example below writes router's MAC address to column _A_ and string _This device is OK_ to column _D_, on sheet _Routers_ in _delivered_routers.xlsx_.

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

There are lots of areas of improvement, which will be addressed sooner or later. Below I listed few most important ones.

**Code**

There's still some repetition in the program's code, and unnecessary commands that don't need to be there (e.g. bash commands). Most of such commands will be replaced with pure Python solutions.

**Installation**

Currently _Cossh_ has to be built from source, but eventually it should be available via _pip_ (.whl).

**Features**

_Cossh_ lacks some features that will be added in future versions, probably the most important will be firmware upgrade, which is coming soon (possible now as well but needs custom commands). Few of the current features also need revamping.
