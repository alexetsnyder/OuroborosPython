#sms.py
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

class TwilioAuth:
	ACCOUNT_SID = ''
	AUTH_TOKEN = ''

class PhoneBook:
	NICK_BOLTON = ''
	ALEX_SNYDER = ''
	TWILIO      = '+19382223913'

class SMS:
	def __init__(self, source_number, account_sid, auth_token):
		self.source_number = source_number
		self.account_sid = account_sid
		self.auth_token = auth_token
		self.proxy = TwilioHttpClient()
		self.proxy.session.proxies = {'https' : os.environ['https_proxy']}
		self.client = Client(self.account_sid, self.auth_token, http_client=self.proxy)

	def send(self, dest_number, msg):
		self.client.messages.create(to=dest_number, from_=self.source_number, body=msg)

def create_reminder(date):
	return 'Reminder: DSA General Meeting on Sunday {0} at 1:30pm to 4:30pm.'.format(date)

if __name__=='__main__':
	import sys
	msg = ''
	dest_number = ''
	sms = SMS(PhoneBook.TWILIO, TwilioAuth.ACCOUNT_SID, TwilioAuth.AUTH_TOKEN)
	if len(sys.argv) == 1:
		msg += 'Hello World From Python!'
		dest_number = PhoneBook.ALEX_SNYDER
	else:
		msg += create_reminder(sys.argv[1])
		dest_number = PhoneBook.ALEX_SNYDER
	sms.send(dest_number, msg)