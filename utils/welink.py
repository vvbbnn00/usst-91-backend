import json
import time
import traceback

import requests
from config import welinkConfig, flaskConfig
from sql import cache

BASE_URL = "https://open.welink.huaweicloud.com/api/"


def get_wlk_token():
    wlk_cache = cache.get("welink_token")
    if wlk_cache:
        return {
            'cached': True,
            'code': 0,
            'message': 'ok',
            'access_token': wlk_cache.decode(),
            'headers': {
                'user-agent': 'usst91 / 1.0 by_bzpl',
                'x-wlk-Authorization': wlk_cache.decode()
            }
        }
    try:
        wlk_token = requests.post(BASE_URL + "auth/v2/tickets", json={
            "client_id": welinkConfig['client_id'],
            "client_secret": welinkConfig['client_secret']
        }).json()
        if int(wlk_token['code']) != 0:
            raise Exception
        cache.set("welink_token", wlk_token['access_token'], ex=int(wlk_token['expires_in'] - 300))
        return {
            'cached': False,
            'code': 0,
            'message': 'ok',
            'token': wlk_token['access_token'],
            'headers': {
                'user-agent': 'usst91 / 1.0 by_bzpl',
                'x-wlk-Authorization': wlk_token['access_token']
            }
        }
    except:
        traceback.print_exc()
        return {
            'code': 500,
            'msg': "Failed to connect to welink."
        }


def get_welink_user(code):
    wlk_token = get_wlk_token()
    if wlk_token['code'] != 0:
        return wlk_token
    headers = wlk_token['headers']
    try:
        user_id = requests.get(BASE_URL + f'auth/v2/userid?code={code}', headers=headers).json()
        if int(user_id['code']) == 41503:
            return {
                'code': 403,
                'msg': 'Unavailable welink code.'
            }
        elif int(user_id['code']) == 0:
            pass
        else:
            cache.delete("welink_token")
            raise Exception(user_id['message'])
        return {
            'code': 0,
            'msg': 'ok',
            'welink_id': user_id['userId']
        }
    except:
        traceback.print_exc()
        return {
            'code': 500,
            'msg': "Failed to connect to welink."
        }


def get_user_data(welink_id):
    wlk_token = get_wlk_token()
    if wlk_token['code'] != 0:
        return wlk_token
    headers = wlk_token['headers']
    try:
        user_data = requests.post(BASE_URL + f'contact/v3/users', json={
            "userId": welink_id
        }, headers=headers).json()
        if int(user_data['code']) == 47001:
            return {
                'code': 400,
                'msg': "Can't find the user."
            }
        elif int(user_data['code']) == 0:
            pass
        else:
            cache.delete("welink_token")
            raise Exception(user_data['message'])
        return {
            'code': 0,
            'msg': 'ok',
            'welink_id': user_data
        }
    except:
        traceback.print_exc()
        return {
            'code': 500,
            'msg': "Failed to connect to welink."
        }


def add_calendar(welink_id, summary, content, location, start_time, end_time, remind_min=0):
    start_time = int(start_time)
    end_time = int(end_time)
    url = BASE_URL + 'calendar/v1/events/add'
    wlk_token = get_wlk_token()
    if wlk_token['code'] != 0:
        return wlk_token
    headers = wlk_token['headers']
    post_data = {
        "receiverUserList": [str(welink_id)],
        'content': str(content),
        'summary': str(summary),
        'location': str(location),
        'startTime': str(start_time),
        'endTime': str(end_time)
    }
    if remind_min > 0:
        post_data['reminder'] = {
            'minutes': str(int(remind_min)),
            'remindType': 'message'
        }
    try:
        calendar_data = requests.post(url, json=post_data, headers=headers).json()
        if int(calendar_data['code']) == 49407:
            return {
                'code': 400,
                'msg': "Failed to operate."
            }
        elif int(calendar_data['code']) == 0:
            pass
        else:
            cache.delete("welink_token")
            raise Exception(calendar_data['message'])
        return {
            'code': 0,
            'msg': 'ok',
            'cal_id': calendar_data['data']['calUid']
        }
    except:
        traceback.print_exc()
        return {
            'code': 500,
            'msg': "Failed to connect to welink."
        }


def edit_calendar(cal_id, welink_id, content, start_time, end_time,
                  summary, location, remind_min=0):
    url = BASE_URL + 'calendar/v1/events/update'
    wlk_token = get_wlk_token()
    if wlk_token['code'] != 0:
        return wlk_token
    headers = wlk_token['headers']
    post_data = {
        "calUid": str(cal_id),
        "receiverUserList": [str(welink_id)],
        'content': "-----------------------------\n"
                   "原先日程信息已发生更改，请注意查看！\n"
                   "-----------------------------\n\n" + str(content),
        'summary': str(summary),
        'location': str(location),
        'startTime': str(int(start_time)),
        'endTime': str(int(end_time))
    }
    if remind_min > 0:
        post_data['reminder'] = {
            'minutes': str(int(remind_min)),
            'remindType': 'message'
        }
    try:
        calendar_data = requests.put(url, json=post_data, headers=headers).json()
        if int(calendar_data['code']) == 49407:
            return {
                'code': 400,
                'msg': "Failed to operate."
            }
        elif int(calendar_data['code']) == 0:
            pass
        else:
            cache.delete("welink_token")
            raise Exception(calendar_data['message'])
        return {
            'code': 0,
            'msg': 'ok'
        }
    except:
        traceback.print_exc()
        return {
            'code': 500,
            'msg': "Failed to connect to welink."
        }


def delete_calendar(cal_id, welink_id):
    url = BASE_URL + 'calendar/v1/events/delete'
    wlk_token = get_wlk_token()
    if wlk_token['code'] != 0:
        return wlk_token
    headers = wlk_token['headers']
    post_data = {
        "calUid": str(cal_id),
        "receiverUserList": [str(welink_id)]
    }
    try:
        calendar_data = requests.post(url, json=post_data, headers=headers).json()
        if int(calendar_data['code']) == 49407:
            return {
                'code': 400,
                'msg': "Failed to operate."
            }
        elif int(calendar_data['code']) == 0:
            pass
        else:
            cache.delete("welink_token")
            raise Exception(calendar_data['message'])
        return {
            'code': 0,
            'msg': 'ok'
        }
    except:
        traceback.print_exc()
        return {
            'code': 500,
            'msg': "Failed to connect to welink."
        }


def get_cache_uid(code):
    if code == "development_header_token" and flaskConfig['ENV'] == 'development':
        return "lutiancheng_659@usst" # debug
    return cache.get("welink_user_code_" + code)
