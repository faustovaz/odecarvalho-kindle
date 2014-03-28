#-*- encoding: utf-8 -*-

import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.MIMEMultipart import MIMEMultipart

config = {
	"email" : "sender@email.com",
	"email-password" : "passwd",
	"email-to" : "email@kindle.com",
	"subject" : "Olavo de Carvalho - Mobi File"
}

def clean():
	""" Deletes the previous mobi file"""
	response = subprocess.call(["rm odecarvalho-artigos.mobi template/pre-kindle-output.html"], shell=True)

def isKindleGenInstalled():
	""" Verifies if kindlegen is available / installed """
	command = subprocess.call(['which kindlegen'], shell=True)
	return not bool(command)

def executeScriptToGenerateFile():
	""" Generates the mobi file """ 
	command = subprocess.call(['python bin/ArticleScrapper.py'], shell=True)
	if not command:
		if os.path.isfile("template/pre-kindle-output.html"):
			command = subprocess.call(['kindlegen template/pre-kindle-output.html -o odecarvalho-artigos.mobi'], shell=True)
			if not command:
				command = subprocess.call(['mv template/odecarvalho-artigos.mobi odecarvalho-artigos.mobi'], shell=True)
		else:
			print "Some error occurred while trying to generate mobi file."

def sendFileToKindleEmail():
	message = MIMEMultipart()
	message['From'] = config['email']
	message['To'] = config['email-to']
	message['Subject'] = config['subject']
	with open('odecarvalho-artigos.mobi', 'rb') as attach:
		mimeApplication = MIMEApplication(attach.read())
	mimeApplication.add_header('Content-Disposition', 'attachment', filename='odecarvalho-artigos.mobi')
	message.attach(mimeApplication)
	mail = smtplib.SMTP('smtp.gmail.com:587')
  	mail.starttls()
	mail.login(config['email'], config['email-password'])
	mail.sendmail(config['email'], config['email-to'], message.as_string())
	mail.close()
	print "Email to %s sent sucessfuly" % config['email-to']


if __name__ == '__main__':
	clean()
	if isKindleGenInstalled():
		executeScriptToGenerateFile()
		if os.path.isfile("odecarvalho-artigos.mobi"):
			sendFileToKindleEmail()
	else:
		print "In order to genereate the mobi file first install kindlegen from Amazon"
