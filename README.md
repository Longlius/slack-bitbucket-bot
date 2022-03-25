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
`config.json` describes the local configuration for the bot. It has three required fields:

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

**`config.json` should be placed in the same directory as `main.py`**

## Setting up the Slack integration
Currently the bot only works for one (1) slack workspace at a time. I don't feel like setting up a full OAuth flow so if you want more, just run multiple instances of the bot.

First go to the [Slack Apps Page](https://api.slack.com/apps) and click **Create New App**

Then go to **OAuth and Permissions** on the new app's dashboard and enable the `chat:write` and `chat:write.public` permissions.

Finally go to **Install App** and install the app to your workspace. The provided OAuth token should be exported as the environment variable `SLACK_OAUTH`. Add the following line to `.env` in the same directory as `main.py`:

```sh
export SLACK_OAUTH=someoauthkeyorsomethingidunno
```

The bot is now ready to send messages to Slack.

## Setting up the Bitbucket integration

You will need a Bitbucket username and a corresponding app password with the correct permissions. Navigate to the [app password page](https://bitbucket.org/account/settings/app-passwords/) on your profile and create a new app password.

Enable read permissions for Projects, Repositories, Pull Requests, Account, Workspace Membership, and Issues. Give the app password a name and write it down.

Add both your bitbucket username and app password to the `BITBUCKET_USER` and `BITBUCKET_PASS` environment variables respectively, or add the following lines to the `.env` file:

```sh
export BITBUCKET_USER=SomeUser
export BITBUCKET_PASS=SomeAppPassword
```

## Running the bot

You can either run `main.py` directly with the correct environment variables defined or, if using `.env`, you can execute the included `run.sh` script to pull the environment variables in and run the bot with the correct command-line arguments.
