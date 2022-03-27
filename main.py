#!/usr/bin/env python3

import slackmessage
import bitbucketmonitor
import json
import sys
import schedule
import time
import os

def main():
	# get configuration parameters from config.json
	workspaces = []
	channel = ""
	jobTime = ""

	isEnvConfigPresent = len(os.environ.get("BITBUCKET_WORKSPACES")) > 0 and len(os.environ.get("SLACK_CHANNEL")) > 0 and len(os.environ.get("POST_TIME")) > 0

	# Get config from environment vars or config.json
	if isEnvConfigPresent:
		workspaces = os.environ.get("BITBUCKET_WORKSPACES").split(",")
		channel = os.environ.get("SLACK_CHANNEL")
		jobTime = os.environ.get("POST_TIME")
	else:
		try:
			f = open("config.json")
			configText = f.read()
			configJson = json.loads(configText)
			workspaces = configJson['bitbucket_workspaces']
			channel = configJson['slack_channel']
			jobTime = configJson['post_time']
		finally:
			f.close()
			if (len(workspaces) == 0) or (channel == "") or (jobTime == ""):
				sys.exit(1)

	# set up the scheduler
	schedule.every().day.at(jobTime).do(jobIteration, workspaces, channel)
	# loop endlessly
	while True:
		schedule.run_pending()
		time.sleep(60)

def jobIteration(workspaces, channel):
	x = monitorPass(workspaces)
	y = generateMarkdownMessages(x)
	z = slackmessage.SlackMessage()
	z.sendBitbucketMarkdownBlock(channel, y)

def monitorPass(workspaces):
	# support multiple bitbucket workspaces if necessary
	monitors = []
	results = []
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

def generateMarkdownMessages(monitorresults):
	markdownStrings = []
	for i in monitorresults:
		markdownStrings.append("<{0}|{1} has {2} unanswered comments(s) in BitBucket.>".format(i[0], i[2], i[3]))
	return markdownStrings


if __name__ == "__main__":
    main()
    sys.exit(0)
