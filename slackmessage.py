# Provides a class to abstract the sending of messages to slack
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackMessage:
	#Token is the OAuth token. Class currently only supports single slack workspace configuration
	def __init__(self, clientId = None, clientSecret = None, botOAuth = None):
		if(clientId is None):
			self.clientId = os.environ.get('SLACK_CLIENT_ID')
		if(clientSecret is None):
			self.clientSecret = os.environ.get('SLACK_CLIENT_SECRET')
		if(botOAuth is None):
			self.botOAuth = os.environ.get('SLACK_OAUTH')
		self.client = WebClient(token=self.botOAuth)
	
	# Sends message to channelName		
	def sendMessage(self, channelName, message):
		try:
			response = self.client.chat_postMessage(channel=channelName, text=message)
		except SlackApiError as e:
			assert e.response["error"]
