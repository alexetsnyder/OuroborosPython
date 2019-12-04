#sms.py
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

class TwilioAuth:
	ACCOUNT_SID = 'ACebead06f395f5d0e36f2984a088f838f'
	AUTH_TOKEN = '943221eca44784a7050835bcf7ecee85'

class PhoneBook:
	NICK_BOLTON = '+15134761150'
	ALEX_SNYDER = '+14194390173'
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