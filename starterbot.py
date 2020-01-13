from slack import RTMClient

SLACK_BOT_TOKEN = "xoxb-842724099156-887681243217-8I5qKgdO4hHv0svR3TWeFeZ5"

# slack_client = slack.WebClient(token=SLACK_BOT_TOKEN)
#slack_client.chat_postMessage(channel="#general",text="hi")

@RTMClient.run_on(event="message")
def hello(**payload):
    data = payload['data']
    web_client = payload['web_client']

    if 'hello' in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text = f"hi <@{user}>!",
            thread_ts = thread_ts
        )

slack_client = RTMClient(token=SLACK_BOT_TOKEN)
slack_client.start()

