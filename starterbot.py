# -*-coding: UTF-8 -*-
from slack import RTMClient
import time
from datetime import date,timedelta
import requests
# SLACK_BOT_TOKEN = "xoxb-45215842257-914671033057-OE22GNVZvKAyYRtkmcp8fewG"
SLACK_BOT_TOKEN = "xoxb-909535567570-910859498035-HfiIg4FUGSNoWlEaPrG2QTKs"
EXCHANGE_RATE_TOKEN = "SpmyBvns5mrR0RfOX1ibVzbkD7e5hT7A"
DARK_API_KEY = "2e23fdad6dbf4d46df180135e48210c5"
BOT_ID = "USA56L8H2"

# Time
TODAY = date.today()
YESTERDAY = date.today() - timedelta(days=1)
TWODAYBEFORE = date.today() - timedelta(days=2)

class exchangeEntity:
    def __init__(self,ttb,tts,base,unit,nation):
        self.nation = nation
        self.ttb = ttb
        self.tts = tts
        self.base = base
        self.unit = unit

    def __str__(self):
        str = ""
        str += "국가: "+self.nation+"\t통화코드: "+self.unit+"\t받으실 때: "+self.ttb+"원\t보내실 때: "\
               +self.tts+"원\t매매 기준: "+self.base + "원\n"
        return str



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

        #if user!=None:
        weatherInfo = weather()
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Hi <@{user}> today weatther at "+weatherInfo['location']+ " is "+weatherInfo['summary']
        )
    elif 'Exchange' in data.get('text',[]):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data.get('user')


        exchage = exchageRate()
        web_client.chat_postMessage(
            channel=channel_id,
            text=f"Hi <@{user}> 물어보신 환율 정보 is 해당 통화 1 단위에 해당하는 한국 원화"+"\n"+exchage
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

    return ret

def exchageRageDataProcessing(dataList):
    ret = {}
    for x in dataList:
        unit = x["cur_unit"]
        if unit == "CNH":
            exchange = exchangeEntity(x["ttb"],x["tts"],x["deal_bas_r"],x["cur_unit"],"중국")
            ret["CNH"] = exchange
        elif unit == "EUR":
            exchange = exchangeEntity(x["ttb"], x["tts"], x["deal_bas_r"], x["cur_unit"],"유럽연합")
            ret["EUR"] = exchange
        elif unit == "GBP":
            exchange = exchangeEntity(x["ttb"], x["tts"], x["deal_bas_r"], x["cur_unit"],"영국")
            ret["GBP"] = exchange
        elif unit == "USD":
            exchange = exchangeEntity(x["ttb"], x["tts"], x["deal_bas_r"], x["cur_unit"],"미국")
            ret["USD"] = exchange
        elif unit == "HKD":
            exchange = exchangeEntity(x["ttb"], x["tts"], x["deal_bas_r"], x["cur_unit"],"홍콩")
            ret["HKD"] = exchange

    return ret

def exchageRate():
    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={EXCHANGE_RATE_TOKEN}&searchdate={date}&data=AP01'

    ret = {}
    toString = ""
    url = url.format(EXCHANGE_RATE_TOKEN=EXCHANGE_RATE_TOKEN,date=TODAY)
    res = requests.get(url).json()
    if res != None:
        ret = exchageRageDataProcessing(res)
        for key in ret:
            toString += ret[key].__str__()+" "
        return toString

    url = url.format(EXCHANGE_RATE_TOKEN=EXCHANGE_RATE_TOKEN, date=YESTERDAY)
    res = requests.get(url).json()
    if res != None:
        ret = exchageRageDataProcessing(res)
        for key in ret:
            toString += ret[key].__str__() + " "
        return toString

    url = url.format(EXCHANGE_RATE_TOKEN=EXCHANGE_RATE_TOKEN, date=TWODAYBEFORE)
    res = requests.get(url).json()
    if res != None:
        ret = exchageRageDataProcessing(res)
        for key in ret:
            toString += ret[key].__str__() + " "
        return toString



if __name__ == "__main__":
    slack_client = RTMClient(
        token=SLACK_BOT_TOKEN,
        connect_method= 'rtm.start'
    )
    slack_client.start()


