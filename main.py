#!/usr/bin/env python3

import slackmessage
import bitbucketmonitor
import json
import sys

def main():
	x = monitorPass()
	
def monitorPass():
	# support multiple bitbucket workspaces if necessary
	monitors = []
	workspaces = []
	results = []
	# open configuration file
	try:
		f = open("config.json")
		configText = f.read()
		configJson = json.loads(configText)
		workspaces = configJson['workspaces']
	finally:
		f.close()
	# check to make sure workspaces was populated
	if len(workspaces) == 0:
		sys.exit(1)
	# Let's make a BitBucketMonitor for each workspace
	for i in workspaces:
		x = bitbucketmonitor.BitBucketMonitor(i)
		monitors.append(x)
	# Now let's run each monitor
	for i in monitors:
		i.unrespondedCommentsPipeline()
		i.preparePullRequestListForOutput()
		x = i.getFinalPullRequestList()
		for j in x:
			results.append(j)
	# return the monitor results
	return results
		
	
if __name__ == "__main__":
    main()
    sys.exit(0)
