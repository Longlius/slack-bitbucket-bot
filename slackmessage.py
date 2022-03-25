# Provides a class to abstract the sending of messages to slack
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackMessage:
	#botOAuth is the OAuth token. Class currently only supports single slack workspace configuration
	def __init__(self, botOAuth = None):
		if(botOAuth is None):
			self.botOAuth = os.environ.get('SLACK_OAUTH')
		self.client = WebClient(token=self.botOAuth)
	
	# Sends message to channelName		
	def sendMessage(self, channelName, message):
		try:
			response = self.client.chat_postMessage(channel=channelName, text=message)
		except SlackApiError as e:
			assert e.response["error"]
			
	# Sends a block message of markdown
	# markdownarr should be an array of markdown strings to send as individual blocks
	def sendBitbucketMarkdownBlock(self, channelName, messagesArr):
		blockarr = []
		for i in messagesArr:
			x = { "type": "section", "text": { "type": "mrkdwn", "text": i } }
			blockarr.append(x)
		try:
			response = self.client.chat_postMessage(channel=channelName, blocks=blockarr)
		except SlackApiError as e:
			assert e.response["error"]
