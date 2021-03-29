#!/usr/bin/env python
from flask import Flask
from flask import request,jsonify
import json
import requests
import re

app = Flask(__name__)

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

class Mailapp:

	def __init__(self):
		self.SG_KEY = "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"
		self.MG_KEY = "f0121fc3d8979f25b2e9e0e7b4235a2d-1553bd45-d99c6cfb"
		self.DUMMY_KEY = "abcd1234"
		self.to_name = "Receiver"
		self.to_email = "muzztestmuzz@gmail.com"
		self.from_name = "Sender"
		self.from_email = "muzzammil@moverobotic.com"
		self.subject = "No Subject"
		self.body = "No Body"
		self.setdown = "default"

	def echeck(self,email):
		if(re.search(regex, email)):
			return True
		else:
			return False

	def send_sendgrid(self):
		url = "https://api.sendgrid.com/v3/mail/send"
		payload = "{\"personalizations\":[{\"to\":[{\"email\":\""+self.to_email+"\",\"name\":\""+self.to_name+"\"}]}], \
		\"from\":{\"email\":\""+self.from_email+"\",\"name\":\""+self.from_name+"\"}, \
		\"reply_to\":{\"email\":\""+self.from_email+"\",\"name\":\""+self.from_name+"\"}, \
		\"subject\":\""+self.subject+"\",\"content\":[{\"type\":\"text/html\",\"value\":\""+self.body+"\"}]}"

		headers = {
		    'authorization': "Bearer "+self.SG_KEY,
		    'content-type': "application/json"
	    }
		return requests.request("POST", url, data=payload, headers=headers)

	def send_mailgun(self):
		return requests.post(
			"https://api.mailgun.net/v3/sandboxdba84c44713f4adeae711693c5079b3d.mailgun.org/messages",
			auth=("api", self.MG_KEY),
			data={
				"to": [self.to_name+"<"+self.to_email+">"],
				"from": self.from_name+"<"+self.from_email+">", 
				"subject": self.subject,
				"html": self.body
				})

	def send(self,data):
		out = self.extract_param(data)
		if out == "1" or out == "2" or out == "3":
			return out
		else: 
			f = self.sending_mail()
			return f

	def extract_param(self,x):
		params = json.loads(x)

		#check existance
		if 'to' not in params:
			return "1"
		elif 'from' not in params:
			return "2"
		elif 'body' not in params:
			return "3"
		elif 'to_name' not in params:
			params['to_name'] = 'Receiver'
		elif 'from_name' not in params:
			params['from_name'] = 'Sender'
		elif 'subject' not in params:
			params['subject'] = 'No Subject'
		elif 'setdown' not in params:
			params['setdown'] = 'default'

		#check empty string
		if params['to'] == '' or self.echeck(params['to']):
			return "1"
		elif params['from'] == '' or self.echeck(params['from']):
			return "2"
		elif params['body'] == '':
			return "3"
		elif params['to_name'] == '':
			params['to_name'] = 'Receiver'
		elif params['from_name'] == '':
			params['from_name'] = 'Sender'
		elif params['subject'] == '':
			params['subject'] = 'No Subject'
		elif params['setdown'] == '' or \
		params['setdown'] != 'default' or \
		params['setdown'] != 'MAILGUN' or \
		params['setdown'] != 'SENDGRID':
			params['setdown'] = 'default'

		self.to_name = params['to_name']
		self.to_email = params['to']
		self.from_name = params['to_name']
		self.from_email = params['from']
		self.subject = params['subject']
		self.body = params['body']
		self.setdown = params['setdown']

		return "OK"


	def sending_mail(self):
		if self.setdown == "MAILGUN":
			self.MG_KEY = self.DUMMY_KEY
		elif self.setdown == "SENDGRID":
			self.SG_KEY = self.DUMMY_KEY

		response = self.send_mailgun()
		if(response.ok==True):
			return "Email Sent With Mailgun"
		else:
			response = self.send_sendgrid()
			if(response.ok==True):
				return "Email Sent with SendGrid"
			else:
				return "4"


@app.route('/')
def index():
	return "API TEST"

@app.route('/email',  methods = ['POST'])
def sendmail():
		sent = False
		MA = Mailapp()
		feedback = MA.send(request.get_data())
		if feedback == "1":
			output = "Target email is compulsory"
		elif feedback == "2":
			output = "Sender email is compulsory"
		elif feedback == "3":
			output = "Email body is compulsory"
		elif feedback == "4":
			output = "Email Sent via MailGun or SendGrid Failed"
		else:
			output = feedback
			sent = True


		if sent == False:
			return json.dumps({"status":False, "response":output, }), 200, {'ContentType':'application/json'}
		else:
			return json.dumps({"status":True, "response":output}), 200, {'ContentType':'application/json'}


if __name__ == '__main__':
   app.debug = True
   app.run(host = '0.0.0.0')


# muzztestmuzz@gmail.com
# muzztestmuzz2021