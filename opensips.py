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
# 2 CRITICAL
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
@copyright: (c) 2012-2013
'''

## Configuration
import sys
import os
import optparse
# from optparse import OptionParser


class OpenSipsModule:
	name = "OpenSipsModule"
	version = '0.1'
	opensipsctl = './opensipsctl_dummy' # OS X
	# opensipsctl = '/usr/local/bin/opensips/sbin/opensipsctl' # production

	options = ''

	def parseOptions(self):
		from optparse import OptionParser
		parser = OptionParser()
		# parser.add_option("-h", "--help", help="print this help")
		parser.add_option("-v", "--version", help="print version and exit")
		parser.add_option("-M", "--metric", dest="metric", help="metric to show")
		parser.add_option("-x", "--exitstatus", dest="state", help="exit with this state")
		parser.add_option("-w", "--warning", dest="threshold_warning", help="set threshold for warning state")
		parser.add_option("-c", "--critical", dest="threshold_critical", help="set threshold for critical state")
		(self.options, args) = parser.parse_args()


	def printVersion(self):
		print '%s %s' % (self.name, self.version)

	def printDebugInfo(self):
		self.printVersion()
		print 'Binary used: %s' % self.opensipsctl

	def checkEnvironment(self):
		# check if specified binary can be used
		print ''

	def __init__(self):
		self.printDebugInfo()
		self.parseOptions()
		sys.exit(OpenSipsModuleStates.OK)



class OpenSipsModuleStates:
	OK = 0
	WARNING = 1
	CRITICAL = 2
	UNKNOWN = 3


if __name__ == '__main__':
	OpenSipsModule()