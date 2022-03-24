import os
import requests
import json

from requests.auth import HTTPBasicAuth

# Handles a single (1) bitbucket workspace.
# Use multiple of these if you want to monitor multiple workspaces
class BitBucketMonitor:
	def __init__(self, workspace, bitbucketuser = None, bitbucketpass = None):
		self.BITBUCKETURL = "https://api.bitbucket.org/2.0/"
		if(bitbucketuser is None):
			self.bitbucketuser = os.environ.get("BITBUCKET_USER")
		if(bitbucketpass is None):
			self.bitbucketpass = os.environ.get("BITBUCKET_PASS")
		self.workspace = workspace
					
	def printRepositories(self):
		response = requests.request("GET", self.BITBUCKETURL+'repositories/Longlius?pagelen=100', auth=HTTPBasicAuth(self.bitbucketuser, self.bitbucketpass))
		print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
		
	# Populates a state variable to hold a list of all repository slugs so we don't have to constantly keep sending GET requests
	def populateRepoSlugList(self, workspace):
		response = requests.request("GET", self.BITBUCKETURL+'repositories/'+workspace+'?pagelen=100', auth=HTTPBasicAuth(self.bitbucketuser, self.bitbucketpass))
		responseParsed = json.loads(response.text)
		acc = []
		for i in responseParsed["values"]:
			acc.append(i["slug"])
		self.reposluglist = acc
	
	# same as populateRepoSlugList but for pull request ids (populateRepoSlugList must be called before invoking this method)
	def populatePullRequestsList(self):
		acc = []
		for i in self.reposluglist:
			currEndpoint = self.BITBUCKETURL + 'repositories/' + self.workspace + '/' + i + '/pullrequests?pagelen=100'
			response = requests.request("GET", currEndpoint, auth=HTTPBasicAuth(self.bitbucketuser, self.bitbucketpass))
			responseParsed = json.loads(response.text)
			for j in responseParsed["values"]:
				acc.append((i, j["id"], j["links"]["html"]))
		self.pullrequestlist = acc
	
	# same as the last two but we're getting comments this time
	def populateCommentsList(self):
		
