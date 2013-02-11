#! /usr/bin/python
#
# Nagios plugin for ASMONIA
# Written by Niels Fallenbeck <niels.fallenbeck@aisec.fraunhofer.de>
# Last modified: 2013-02-11
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
#	asmonia -M active_dialogs -w 10 -c 50
'''
@author: Niels Fallenbeck <niels.fallenbeck@aisec.fraunhofer.de>
@copyright: (c) 2012-2013
'''

## Configuration
import sys
import os
import optparse
import re
from subprocess import PIPE
from subprocess import Popen
from decimal import Decimal
from optparse import OptionParser


class OpenSipsModule:
	name = "OpenSipsModule"
	version = '0.1'
	# opensipsctl = '/usr/local/bin/opensips/sbin/opensipsctl' # production
	opensipsctl = './opensipsctl_dummy' # opensipsctl dummy for testing purposes

	# default settings
	threshold_warning = 2
	threshold_critical = 5
	exitstatus = 3 #OpenSipsModuleStates.UNKNOWN
	test = False

	# Metrics settings
	metric = "all"
	description = ""
	value = -1


	def parse_options(self):
		# command line option parsing
		parser = OptionParser()
		parser.add_option("-v", "--version", action="store_true", dest="show_version", default=False, help="print version and exit")
		parser.add_option("-t", "--test", action="store_true", dest="test_config", default=False, help="test if configuration is working")
		parser.add_option("-M", "--metric", dest="metric", default="all", help="metric to show")
		parser.add_option("-x", "--exitstatus", dest="state", default=3, help="exit with this state")
		parser.add_option("-w", "--warning", dest="threshold_warning", default=2, help="set threshold for warning state")
		parser.add_option("-c", "--critical", dest="threshold_critical", default=5, help="set threshold for critical state")
		(self.options, args) = parser.parse_args()

		# store options to global variables
		self.metric = self.options.metric
		self.description = self.get_metric_description(self.metric)
		self.threshold_warning = Decimal(self.options.threshold_warning)
		self.threshold_critical = Decimal(self.options.threshold_critical)
		self.exitstatus = Decimal(self.options.state)


	def print_version(self):
		# Just print the version
		print '%s %s' % (self.name, self.version)


	def check_config(self):
		# check if specified binary can be used
		print 'check system environment...'
		print '  binary used as configured in script: %s' % self.opensipsctl
		try:
			# check if file is there and can be opened
   			with open(self.opensipsctl) as f: 
   				# call the binary and see what happens
				x = Popen('%s 1 2 all' % self.opensipsctl, stdout=PIPE, stderr=PIPE, shell=True)
				output, errors = x.communicate()
				if x.returncode:
					print 'Error: %s' % errors
					self.exitstatus = 2
				else:
					print '  opensipsctl binary found.'
		except IOError as e:
   			print 'Error: %s' % e
   			self.exitstatus = 1
   		print "  metric to parse:    %s" % self.metric
   		print "  threshold WARNING:  %d" % self.threshold_warning
   		print "  threshold CRITICAL: %d" % self.threshold_critical
   		print "  exit status:        %s" % self.exitstatus
   		exit(self.exitstatus)


   	def get_metric_description(self, metric):
   		# Provide a human-readable description of the given metric
   		
   		# Metrics which are not supported must be specified here
   		if metric == "udp-load":
   			print "Metric %s not supported!" % (metric)
   			exit(OpenSipsModuleStates.UNKNOWN)

   		try:
   			return {
				"rcv_requests"			:	"received requests",
				"rcv_replies"			:	"received replies",
				"fwd_requests"			:	"forwarded requests",
				"fwd_replies"			:	"forwarded replies",
				"drop_requests"			:	"droped requests",
				"drop_replies"			:	"dropped replies",
				"err_requests"			:	"bogus replies",
				"err_replies"			:	"bogus replies",
				"bad_URIs_rcvd"			:	"bad URIs received",
				"unsupported_methods"	:	"non-standard methods encountered",
				"bad_msg_hdr"			:	"bad SIP headers",
				"timestamp"				:	"seconds running",
				"tcp-load"				:	"TCP load",
				"waiting_udp"			:	"UDP waiting buffer size",
				"waiting_tcp"			:	"TCP waiting buffer size",
				"waiting_tls"			:	"TLS waiting buffer size",
				"total_size"			:	"total shared memory",
				"used_size"				:	"used shared memory",
				"real_used_size"		:	"used real shared memory (including malloc overhead)",
				"max_used_size"			:	"maximum used memory",
				"free_size"				:	"free shared memory",
				"fragments"				:	"shared memory fragments",
				"1xx_replies"			:	"1xx replies",
				"2xx_replies"			:	"2xx replies",
				"3xx_replies"			:	"3xx replies",
				"4xx_replies"			:	"4xx replies",
				"5xx_replies"			:	"5xx replies",
				"6xx_replies"			:	"6xx replies",
				"sent_replies"			:	"sent replies",
				"sent_err_replies"		:	"sent bogus replies",
				"received_ACKs"			:	"received ACKs",
				"received_replies"		:	"received replies",
				"relayed_replies"		:	"relayed replies",
				"local_replies"			:	"local replies",
				"UAS_transactions"		:	"transactions created by received requests",
				"UAC_transactions"		:	"transactions created by local generated requests",
				"2xx_transactions"		:	"transactions completed with 2xx replies",
				"3xx_transactions"		:	"transactions completed with 3xx replies",
				"4xx_transactions"		:	"transactions completed with 4xx replies",
				"5xx_transactions"		:	"transactions completed with 5xx replies",
				"6xx_transactions"		:	"transactions completed with 6xx replies",
				"inuse_transactions"	:	"transactions existing in memory",
				"positive_checks"		:	"tests executed for which a positive match",
				"negative_checks"		:	"tests executed for which a negative match",
				"registered_users"		:	"users in memory for all domains",
				"location-users"		:	"users in memory",
				"location-contacts"		:	"contacts in memory",
				"location-expires"		:	"expired contacts in memory",
				"max_expires"			:	"max expiration",
				"max_contacts"			:	"max contacts",
				"default_expire"		:	"default expiration",
				"accepted_regs"			:	"accepted registrations",
				"rejected_regs"			:	"rejected registrations",
				"active_dialogs"		:	"current active dialogs",
				"early_dialogs"			:	"early dialogs",
				"processed_dialogs"		:	"processed dialogs",
				"expired_dialogs"		:	"expired dialogs",
				"failed_dialogs"		:	"failed dialogs",
   			}[metric]
   		except Exception as e:
   			print "Unknown metric %s" % (metric)
   			exit(OpenSipsModuleStates.UNKNOWN)


   	def get_metric(self):
   		# execute output
   		x = Popen('%s fifo get_statistics %s' % (self.opensipsctl, self.metric), stdout=PIPE, stderr=PIPE, shell=True)
   		output, errors = x.communicate()
   		if x.returncode != 0:
   			#print 'Error: %s' % errors
   			exit(self.exitstatus)

   		# now we need to parse the output
   		c = re.compile(r"%s" % self.metric)
   		# result = [c.findall(line) for line in output.splitlines(False)]
   		# print(result)
   		for line in output.splitlines(False):
   			# if re.search(r"%s" % self.metric, line):
   			if c.findall(line):
   				self.value = Decimal(line.split(" ")[2])
   				break


   	def generate_result(self):
   		# compare value with thresholds
   		prefix = "openSIPS"
   		state = "UNKNOWN"

   		if self.value < 0:
   			state = "UNKNOWN"
   			self.exitstatus = OpenSipsModuleStates.UNKNOWN
   		elif self.value >= self.threshold_critical:
   			state = "CRITICAL"
   			self.exitstatus = OpenSipsModuleStates.CRITICAL
   		elif self.value >= self.threshold_warning:
   			state = "WARNING"
   			self.exitstatus = OpenSipsModuleStates.WARNING
   		else:
   			state = "OK"
   			self.exitstatus = OpenSipsModuleStates.OK

   		# exit the script
   		print "%s %s - %d %s" % (prefix, state, self.value, self.description)
   		exit(self.exitstatus)



	def __init__(self):
		# first, parse the options
		self.parse_options()

		# and then deal with it
		if self.options.show_version:
			self.print_version()
		elif self.options.test_config:
			self.print_version()
			self.check_config()
		else:
			self.get_metric()
			self.generate_result()

		# if you are here, everything went fine!
		sys.exit(OpenSipsModuleStates.OK)



# Define the exit codes of the various states
class OpenSipsModuleStates:
	OK = 0
	WARNING = 1
	CRITICAL = 2
	UNKNOWN = 3


# If called from the command line simply create a new OpenSipsModule instance
if __name__ == '__main__':
	OpenSipsModule()