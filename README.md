PIPA STREAM 3rd GENERATION
==========================

Description
-----------
There is configuration and runners for pipa stream 3rd generation based on
[rocketeer](https://github.com/offlinehacker/rocketeer) remote process launcher, watchdog and manager.

Installation
-----------
- Install newest stable ffmpeg from git. This site is example how to do it on ubuntu [FFmpeg ubuntu](http://ubuntuforums.org/showthread.php?t=786095)
- Install liblirc using apt-get install liblircclient-dev.
- Install this package using python setup.py install.
- if you want to start on system startup there are init script avalible in init folder and sample lirc config in config folder.
- Copy init scripts to /etc/init.d/
- Copy config files to /etc/pstream/

FAQ:
----
- Problems with paramiko:
If you have any problems with paramiko library, on which stream is dependant on use pip install paramiko and it should work.

Usage:
------
There are two cli commands(add --help for more info):

- stream3d - xml-rpc app server.
- rocketeer-client - command line client for server, refer to rocketeer documentation for usage.
- stream3-lirc - lirc client for server.

License:
--------
Pipa_stream3 is Copyright (C) 2011 kiberpipa.

Pipa_stream3 is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License version 2 as published by the Free Software Foundation.

Pipa_stream3 is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
