#! /usr/bin/python
#
# Nagios plugin for ASMONIA
# Written by Niels Fallenbeck <niels.fallenbeck@aisec.fraunhofer.de>
# Last modified: 2012-12-30
# 
# Usage: ./asmonia.py
#
# Description
# This plugin returns the state of the opensips SIP server
#
# Output
# Depending on the threshold it will return the appropriate state of 
# server. It will provide information about the current utilization
# and will exit with a code corresponding to its state.
# O OK
# 1 WARNING
# 2 ERROR
# 3 UNKNOWN
# 
# Notes:
# There are some standard thresholds defined which will be used if
# no thresholds will be defined during the script's call
#
# Examples:
# Check for logged in users and return warning state at 10 and
# critical state at 50:
#	asmonia -M users -w 10 -c 50
'''
@author: Niels Fallenbeck <niels.fallenbeck@aisec.fraunhofer.de>
@copyright: (c) 2012 
'''

## Configuration
import sys
import os

class OpenSipsModule

	var version="0.1"

	def ___init___(self):
		print version
