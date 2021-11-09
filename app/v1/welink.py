import datetime

import werkzeug.exceptions

from config import apiConfig
from sql import cache
from sql.recruitment import count_recruitment
from sql.meet_table import count_meet_table
from utils.error import gen_error_msg
from utils.welink import get_cache_uid
from sql.calendar import *
from flask import *

import time

bp = Blueprint('v1_welink', __name__, url_prefix='/welink')


@bp.route("/card", methods=["get"])
def http_get_welink_card():
    start_ts = time.time() * 1000
    cache_data = cache.get("welink_card")
    cached = False
    if cache_data:
        cache_data = json.loads(cache_data)
        today_cru = cache_data['today_cru']
        tomorrow_cru = cache_data['tomorrow_cru']
        today_meet = cache_data['today_meet']
        cached = True
    else:
        today = datetime.date.today()
        tomorrow = datetime.date.fromtimestamp(time.time() + 86400)

        today_cru = count_recruitment(start_date=today, end_date=today)
        tomorrow_cru = count_recruitment(start_date=tomorrow, end_date=tomorrow)
        today_meet = count_meet_table(start_date=today, end_date=today)

        today_cru = "获取失败" if today_cru['code'] != 0 else str(today_cru['total'])
        tomorrow_cru = "获取失败" if tomorrow_cru['code'] != 0 else str(tomorrow_cru['total'])
        today_meet = "获取失败" if today_meet['code'] != 0 else str(today_meet['total'])
        if today_cru != "获取失败" and tomorrow_cru != "获取失败" and today_meet != "获取失败":
            cache.set("welink_card", json.dumps({
                'today_meet': today_meet,
                'tomorrow_cru': tomorrow_cru,
                'today_cru': today_cru
            }), ex=3600)

    time_cost = time.time() * 1000 - start_ts
    return {
        "cached": cached,
        "timeCost": time_cost,
        "type": "market_card_store_nine_indicator",
        "content": {
            "colCount": 3,
            "data": [
                {
                    "type": "market_item_store_nine_indicator",
                    "title": "今日宣讲会",
                    "action": "h5://20211018231353983577841/index.html",
                    "number": today_cru,
                    "unit": "场",
                    "numberColor": "#333333",
                    "titleColor": "#999999"
                }, {
                    "number": tomorrow_cru,
                    "unit": "场",
                    "numberColor": "#333333",
                    "action": "h5://20211018231353983577841/index.html",
                    "title": "明日宣讲会",
                    "unitColor": "#999999",
                    "type": "market_item_store_nine_indicator"
                }, {
                    "number": today_meet,
                    "unit": "场",
                    "numberColor": "#333333",
                    "title": "今日招聘会",
                    "action": "h5://20211018231353983577841/index.html",
                    "unitColor": "#999999",
                    "type": "market_item_store_nine_indicator"
                }
            ]
        }
    }


@bp.route("/subscription/list", methods=["post"])
def http_get_calendar_list():
    welink_id = get_cache_uid(request.headers.get('x-wlk-code'))
    error_list = []
    try:
        limit = int(request.form.get("limit") if request.form.get("limit") else 20)
        limit = 500 if limit > 500 else limit
        limit = 1 if limit < 1 else limit
    except:
        error_list.append("Illegal param 'limit', it should be an integer.")
    try:
        q_from = int(request.form.get("from") if request.form.get("from") else 0)
        if q_from > 2147483647 or q_from < 0:
            error_list.append("Illegal param 'from', it should be an integer.")
    except:
        error_list.append("Illegal param 'from', it should be an integer.")
    if len(error_list) > 0:
        return gen_error_msg(error_list, 400)

    data = get_sub_list(welink_id=welink_id, limit=limit, q_from=q_from)
    if data['code'] != 0:
        return data
    for index in range(len(data['data'])):
        data['data'][index].__delitem__("cal_id")
    data.__delitem__("code")
    return {
        'code': 0,
        'msg': 'ok',
        'result': data
    }


@bp.route("/subscription/add", methods=["post"])
def http_add_calendar():
    welink_id = get_cache_uid(request.headers.get('x-wlk-code'))
    error_list = []
    try:
        sub_type = int(request.form.get("sub_type"))
        if sub_type not in [0, 1]:
            raise Exception
    except:
        error_list.append("Illegal param 'sub_type', it should be an integer in [0,1].")
    try:
        sub_id = request.form["sub_id"]
    except:
        error_list.append("Param 'sub_id' is required.")

    if len(error_list) > 0:
        return gen_error_msg(error_list, 400)

    data = create_sub_item(welink_id=welink_id, sub_type=sub_type, sub_id=sub_id)
    if data['code'] != 0:
        return data
    return {
        'code': 0,
        'msg': 'ok'
    }


@bp.route("/subscription/delete", methods=["post"])
def http_delete_calendar():
    welink_id = get_cache_uid(request.headers.get('x-wlk-code'))
    error_list = []
    try:
        sub_type = int(request.form.get("sub_type"))
        if sub_type not in [0, 1]:
            raise Exception
    except:
        error_list.append("Illegal param 'sub_type', it should be an integer in [0,1].")
    try:
        sub_id = request.form["sub_id"]
    except:
        error_list.append("Param 'sub_id' is required.")

    if len(error_list) > 0:
        return gen_error_msg(error_list, 400)

    data = delete_sub(welink_id=welink_id, sub_type=sub_type, sub_id=sub_id)
    if data['code'] != 0:
        return data
    return {
        'code': 0,
        'msg': 'ok'
    }


@bp.route("/sys/update")
def http_update_data():
    api_token = request.args.get("key")
    if api_token != apiConfig['token']:
        raise werkzeug.exceptions.NotFound
    import _thread
    _thread.start_new_thread(update_data, ())
    return {
        'code': 0,
        'msg': 'ok'
    }
