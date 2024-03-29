import json
import os
import hoshino
import re
from hoshino import Service, priv
from hoshino import aiorequests
from hoshino.util import FreqLimiter, escape
from hoshino.typing import CQEvent


sv = Service('livewatcher', bundle='直播间订阅')

config_path = './hoshino/modules/livewatcher/watcher-config.json'

ytb_url = "https://www.youtube.com/channel"

CEHCK_FALG = 'icon":{"iconType":"LIVE"}'

uid_cache = []


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

def load_config():
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf8') as config_file:
                return json.load(config_file)
        else:
            return {}
    except:
        return {}

def save_config(config):
    try:
        with open(config_path, 'w', encoding='utf8') as config_file:
            json.dump(config, config_file, ensure_ascii=False, indent=4)
        return True
    except BaseException as e:
        return False

async def getStatus(userId):
    url = "https://api.bilibili.com/x/space/app/index?mid=" + userId
    resp = await aiorequests.get(url,timeout=10, stream=True, headers=headers)
    res = await resp.json()
    return res

async def get_ytb_status(channelId):
    REGEX = f'(?<="channelId":"{channelId}","title":)".*"(?=,"navigationEndpoint")'
    result = {'status':'0'}
    resp = await aiorequests.get(f'{ytb_url}/{channelId}')
    resp_text = await resp.text
    match = re.findall(REGEX, resp_text)
    if match is not None:
        result['title'] = match
    if CEHCK_FALG in resp_text:
        result['status'] = '1'
    return result

async def sendPublic(userList, message):
    bot = hoshino.get_bot()
    #await bot.send_private_msg(user_id=2452473343,message=message)
    for user in userList:
        await bot.send_group_msg(group_id=int(user), message=message)

def checkFlag(config):
    if config['flag'] == "true":
        return True
    else:
        return False

@sv.on_prefix('增加直播监听')
async def addWatcher(bot, ev: CQEvent):
    config = load_config()
    roomId = escape(ev.message.extract_plain_text().strip())
    if roomId in config:
        if str(ev.group_id) not in config[roomId]['group']:
            config[roomId]['group'].append(str(ev.group_id))
    else:
        config[roomId] = {}
        group = [str(ev.group_id)]
        config[roomId]['group'] = group
        config[roomId]['notification'] = 'true'
        config[roomId]['flag'] = 'false'
    if save_config(config):
        await bot.send_group_msg(group_id=ev.group_id, message='添加成功')
    else:
        await bot.send_group_msg(group_id=ev.group_id, message='添加失败')

@sv.on_prefix('删除直播监听')
async def delWatcher(bot, ev: CQEvent):
    config = load_config()
    roomId = escape(ev.message.extract_plain_text().strip())
    if roomId in config:
        if str(ev.group_id) in config[roomId]['group']:
            config[roomId]['group'].remove(str(ev.group_id))
            await bot.send_group_msg(group_id=ev.group_id, message='删除成功')
    save_config(config)

@sv.scheduled_job('interval', seconds=int(120))
async def search():
    config = load_config()
    for userId in config.keys():
        if userId.isdigit():
            res = await getStatus(userId)
            status = res['data']['info']['live']['liveStatus']
            room = config[userId]
            if checkFlag(room):
                if status == 0:
                    room['flag'] = 'false'
                    save_config(config)
            else:
                if status == 1:
                    room['flag'] = 'true'
                    save_config(config)
                    message = await createBiliMessage(res['data']['info'])
                    if(config[userId]['notification']=='true'):
                        message = f'[CQ:at,qq=all] {message}'
                    await sendPublic(config[userId]['group'], message)
        else:
            result = await get_ytb_status(userId)
            room = config[userId]
            if checkFlag(room):
                if result['status'] == '0':
                    room['flag'] = 'false'
                    save_config(config)
            else:
                if result['status'] == '1':
                    room['flag'] = 'true'
                    save_config(config)
                    message = await createYtbMessage(result['title'])
                    if(config[userId]['notification']=='true'):
                        message = f'[CQ:at,qq=all] {message}'
                    await sendPublic(config[userId]['group'], message)

async def createBiliMessage(data):
    message = f"{data['name']}开播了!\n{data['live']['title']}\n{data['live']['url']}"
    return message

async def createYtbMessage(title):
    message = f"您关注的{title}开播了!"
    return message
