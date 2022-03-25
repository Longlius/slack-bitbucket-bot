# slack-bitbucket-bot
A python 3 bot for posting updates about unanswered comments on bitbucket in a slack channel.

## Python dependencies
Install the following dependencies via pip:

```
pip install requests
pip install slack_sdk
pip install schedule
```

## config.json
config.json describes the local configuration for the bot. It has three required fields:

1. `workspaces` - This is an array of strings. Each string corresponds to a BitBucket workspace to monitor.
2. `channel` - This is a single string. It corresponds to the slack channel the bot will post digests in.
3. `time` - This is a single string. It correponds to a single time of day that the bot will run.

For example, if we wanted to get information about workspace `Longlius` at noon every day and post it in the `engineering` channel, config.json would look like this:

```json
{
	"workspaces": [
		"Longlius"
	],
	"channel": "engineering",
	"time": "12:00"
}
```

## Setting up the Slack integration
Currently the bot only works for one (1) slack workspace at a time. I don't feel like setting up a full OAuth flow so if you want more, just run multiple instances of the bot.


