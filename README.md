# POSSUM_target_alert

A script that checks the POSSUM observation status of a list of target sources

Once a new target has been observed, announce on the POSSUM Slack channel via Slack bot

Best to run this periodically (weekly?) via e.g. `cron`



## Example Output

To-be-added...



## If you want to use this on the POSSUM Slack channel

Please feel free to contact Jackie (on Slack, or e-mail) to set this up!

If you can provide an input source list (in identical format as the `POSSUM` script maintained by Craig Anderson), Jackie can set up a `cron` job to run this periodically, and send the results to you directly via Slack DM, or to a particular Slack channel

If you would like more flexibility and set this up on your own using your machine, Jackie can test things out to make sure the script attaches to the POSSUM Slack properly



## Installation

```
git clone https://github.com/jackieykma/POSSUM_target_alert.git
cd POSSUM_target_alert
git clone https://github.com/candersoncsiro/POSSUM.git
```
The above command downloads this `POSSUM_target_alert` script, as well as the `POSSUM` script maintained by Craig Anderson that this script depends on



## Some notes for setting up Slack token

For this script to work properly, the user needs to set up the Slack Bot User OAuth Token in the shell environment. For example,
```
export SLACK_TOKEN=xoxb-xxxxxxxxxxxxxxxxxxxxxxxxxx
```
This can either be set before executing the `POSSUM_target_alert` script, or provided to the shell profile

The script will then read the Slack token automatically



## Other useful information

Some good resources for setting up a Slack message bot: 

https://www.datacamp.com/tutorial/how-to-send-slack-messages-with-python

https://api.slack.com/methods/chat.postMessage
