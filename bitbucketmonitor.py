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
		self.commentswithoutresponse = []
					
	def printRepositories(self):
		response = requests.request("GET", self.BITBUCKETURL+'repositories/Longlius?pagelen=100', auth=HTTPBasicAuth(self.bitbucketuser, self.bitbucketpass))
		print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
		
	# Populates a state variable to hold a list of all repository slugs so we don't have to constantly keep sending GET requests
	def populateRepoSlugList(self):
		acc = []
		nextPageUrl = self.BITBUCKETURL+'repositories/'+self.workspace+'?pagelen=100'
		while nextPageUrl is not None:
			response = requests.request("GET", nextPageUrl, auth=HTTPBasicAuth(self.bitbucketuser, self.bitbucketpass))
			responseParsed = json.loads(response.text)
			for i in responseParsed["values"]:
				acc.append(i["slug"])
			nextPageUrl = responseParsed.get('next', None)
		self.reposluglist = acc
	
	# same as populateRepoSlugList but for pull request ids (populateRepoSlugList must be called before invoking this method)
	def populatePullRequestsList(self):
		acc = []
		for i in self.reposluglist:
			nextPageUrl = self.BITBUCKETURL + 'repositories/' + self.workspace + '/' + i + '/pullrequests?pagelen=100'
			while nextPageUrl is not None:
				response = requests.request("GET", nextPageUrl, auth=HTTPBasicAuth(self.bitbucketuser, self.bitbucketpass))
				responseParsed = json.loads(response.text)
				for j in responseParsed["values"]:
					acc.append((i, j["id"], j["links"]["html"]))
				nextPageUrl = responseParsed.get('next', None)
		self.pullrequestlist = acc
	
	# same as the last two but we're getting comments this time (populatePullRequestsList needs to be run before this)
	def populateCommentsList(self):
		acc = []
		# oh boy
		for i in self.pullrequestlist:
			# may god have mercy on my soul
			nextPageUrl = self.BITBUCKETURL + 'repositories/' + self.workspace + '/' + i[0] + '/pullrequests/' + i[1] + '/comments?pagelen=100'
			while nextPageUrl is not None:
				response = requests.request("GET", nextPageUrl, auth=HTTPBasicAuth(self.bitbucketuser, self.bitbucketpass))
				responseParsed = json.loads(response.text)
				for j in reponseParsed["values"]:
					acc.append((i, j))
				nextPageUrl = responseParsed.get('next', None)
		self.commentslist = acc
	
	# okay this next part is going to be hella hacky because bitbucket's api is terrible
	# we need to find all top-level comments without responses
	# logically
	# T = {all comments C st C does not have a parent AND there does not exist a comment C' whose parent is C}
	# In this case, T is the set of all comments that have not been responded to
	
	# first let's get all top-level comments
	# that is to say - all comments without parents
	def topLevelComments(self):
		acc = []
		for i in self.commentslist:
			x = i[1].get('parent', None)
			if x is None:
				acc.append(i)
		self.toplevelcomments = acc
		
	def unrespondedComments(self):
		#first let's go through the comments and pull out every parent comment's id
		acc1 = []
		for i in self.commentslist:
			x = i[1].get('parent', None)
			if x is not None:
				acc1.append(i[1]['parent']['id'])
		# Now let's remove every comment in self.toplevelcomments whose id matches an id in acc1
		for i in self.toplevelcomments:
			for j in acc1:
				if i[1]['id'] == j:
					self.toplevelcomments.remove(i)
	
	
		
