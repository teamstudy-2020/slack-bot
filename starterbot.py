# -*-coding: UTF-8 -*-
from slack import RTMClient
from flask import Flask
from flask import Response
import time
import requests

SLACK_BOT_TOKEN = ""
DARK_API_KEY = "2e23fdad6dbf4d46df180135e48210c5"
BOT_ID = "USA56L8H2"

@RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']
    #rtm_client = payload['rtm_client']
    if 'Hello' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Hi <@{user}>!",
            thread_ts=thread_ts
        )

    elif 'weather' in data.get('text',[]):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data.get('user')

        if user!=None:
            weatherInfo = weather()
            web_client.chat_postMessage(
                channel=channel_id,
                text=f"Hi <@{user}> today weather at "+weatherInfo['location']+ " is "+weatherInfo['summary'],
                thread_ts=thread_ts
            )



def weather():
    lat = 37.516252
    vlong = 127.023549
    url  = 'https://api.darksky.net/forecast/{DARK_API_KEY}/{lat},{vlong}?lang=ko&units=si'
    url = url.format(DARK_API_KEY = DARK_API_KEY,lat=lat,vlong=vlong)
    res = requests.get(url).json()
    a= res['currently']
    ret = {}
    ret['location'] = 'Sinchon'
    ret['curentTime'] = time.ctime(a['time'])
    ret['summary'] = a['summary']
    ret['apparentTemperature'] = a['apparentTemperature']
    ret['temperature'] = a['temperature']
    #ret = json.dumps(ret).encode('utf8')
    #return Response(ret,content_type='application/json; charset=utf-8')
    return ret


if __name__ == "__main__":
    slack_client = RTMClient(
        token=SLACK_BOT_TOKEN,
        connect_method= 'rtm.start'
    )
    slack_client.start()


