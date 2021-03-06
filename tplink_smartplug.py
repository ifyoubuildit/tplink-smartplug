#!/usr/bin/env python2
#
# TP-Link Wi-Fi Smart Plug Protocol Client
# For use with TP-Link HS-100 or HS-110
#
# by Lubomir Stroetmann
# Copyright 2016 softScheck GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import json
import os
import socket
import sys

from struct import pack
from os import path

os.chdir("/Users/branclx1/GitHub/forked/tplink-smartplug")
sys.path.append(path.abspath('../../../GitLab/personal/utils'))
from common import misc

version = 0.3

# Check if hostname is valid
def validHostname(hostname):
	try:
		socket.gethostbyname(hostname)
	except socket.error:
		parser.error("Invalid hostname.")
	return hostname

# Predefined Smart Plug Commands
# For a full list of commands, consult tplink_commands.txt
# {"system":{"get_sysinfo":{}},"emeter":{"get_realtime":{}},"time":{"get_time":{}}}
commands = {'info'     : '{"system":{"get_sysinfo":{}}}',
			'on'       : '{"system":{"set_relay_state":{"state":1}}}',
			'off'      : '{"system":{"set_relay_state":{"state":0}}}',
			'cloudinfo': '{"cnCloud":{"get_info":{}}}',
			'wlanscan' : '{"netif":{"get_scaninfo":{"refresh":0}}}',
			'time'     : '{"time":{"get_time":{}}}',
			'schedule' : '{"schedule":{"get_rules":{}}}',
			'countdown': '{"count_down":{"get_rules":{}}}',
			'antitheft': '{"anti_theft":{"get_rules":{}}}',
			'reboot'   : '{"system":{"reboot":{"delay":1}}}',
			'reset'    : '{"system":{"reset":{"delay":1}}}',
			'energy'   : '{"emeter":{"get_realtime":{}}}'
}
def encrypt(string):
	key = 171
	result = b"\0\0\0" + bytes([len(string)])
	for i in string.encode('latin-1'):
		a = key ^ i
		key = a
		result += bytes([a])
	return result
	
def decrypt(string):
	key = 171
	result = b""
	for i in string:
		a = key ^ i
		key = i
		result += bytes([a])
	return result.decode('latin-1')

# Parse commandline arguments
parser = argparse.ArgumentParser(description="TP-Link Wi-Fi Smart Plug Client v" + str(version))
parser.add_argument("-t", "--target", metavar="<hostname>", required=True, help="Target hostname or IP address", type=validHostname)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-c", "--command", metavar="<command>", help="Preset command to send. Choices are: "+", ".join(commands), choices=commands)
group.add_argument("-j", "--json", metavar="<JSON string>", help="Full JSON string of command to send")
args = parser.parse_args()

logger = misc.my_logger(('./log/tplink-smartplug_{}.log').format(misc.get_dt(fmt='yyyymmdd')))
logger.info({"action":"start"})
# Set target IP, port and command to send
ip = args.target
port = 9999

logger.info({"ip":ip,"port":port,"command":str(args.command)})

if args.command is None:
	cmd = args.json
else:
	cmd = commands[args.command]

# Send command and receive reply
try:
	sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_tcp.connect((ip, port))
	sock_tcp.send(encrypt(cmd))
	data = sock_tcp.recv(2048)
	sock_tcp.close()

	output = json.loads(decrypt(data[4:]))
	output = {
		"device":{
			"ip": ip
		},
		"meta":{
			"date":misc.get_dt(fmt='yyyymmddHHMM')
		},
		"data":output
	}
	output_path = './output/' + str(args.command) + '/' + str(misc.get_dt(fmt='yyyymmdd')) + '/'
	misc.file_write(fname= output_path + str(ip).replace('.','_') + '_' + misc.get_dt(fmt='yyyymmddHHMMSS') + '.json',fformat='json',data=output,pprint=True)
	logger.info({"action":"end"})
except socket.error:
	message = {"message":"Cound not connect to host " + ip + ":" + str(port)}
	logger.error(message)
	print(message)
	sys.exit(1)

