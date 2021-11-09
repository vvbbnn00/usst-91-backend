from flask import *
from sql.recruitment import *
from sql.calendar import get_sub_list
from sql import cache
import re

from utils.welink import get_cache_uid

re_date = r"\d{4}-\d{2}-\d{2}"

bp = Blueprint('v1_recruitment', __name__, url_prefix='/recruit')


@bp.route("/query", methods=["POST"])
def http_query_recruitment():
    start_timestamp = time.time() * 1000

    error_list = []
    start_date = request.form.get("date_start")
    end_date = request.form.get("date_end")
    date_order = "desc" if not request.form.get("date_order") else request.form.get("date_order")
    return_status = request.form.get("return_status")
    if return_status:
        max_limit = 30
    else:
        max_limit = 500
    if not ['asc', 'desc'].__contains__(date_order):
        error_list.append("Illegal param 'date_order', it should be 'asc' or 'desc'.")

    if not start_date or not end_date:
        error_list.append("Param 'date_start' and 'date_end' is required.")
        return gen_error_msg(error_list, 400)

    if not re.match(re_date, start_date):
        error_list.append("Illegal param 'date_start', it should be like '2021-01-01'.")
    if not re.match(re_date, end_date):
        error_list.append("Illegal param 'date_end', it should be like '2021-01-01'.")

    try:
        limit = int(request.form.get("limit") if request.form.get("limit") else 20)
        limit = max_limit if limit > max_limit else limit
        limit = 1 if limit < 1 else limit
    except:
        error_list.append("Illegal param 'limit', it should be an integer.")
    try:
        if request.form.get("page"):
            page = int(request.form.get("page"))
        else:
            page = int(request.form.get("from") if request.form.get("from") else 0)
        if page > 2147483647 or page < 0:
            error_list.append("Illegal param 'page', it should be an integer.")
    except:
        error_list.append("Illegal param 'page', it should be an integer.")

    if len(error_list) > 0:
        return gen_error_msg(error_list, 400)

    cache_data = cache.get(f"http_query_recruitment_{start_date}_{end_date}_{date_order}_{limit}_{page}")
    if cache_data:
        result = json.loads(cache_data)
        cached = True
    else:
        result = query_recruitment(start_date=start_date, end_date=end_date, limit=limit,
                                   page=page, date_order=date_order)
        if result['code'] != 0:
            return result
        result.__delitem__('code')
        cache.set(f"http_query_recruitment_{start_date}_{end_date}_{date_order}_{limit}_{page}",
                  json.dumps(result), ex=300)
        cached = False

    if return_status:
        welink_id = get_cache_uid(request.headers.get('x-wlk-code'))
        for index in range(len(result['data'])):
            query_id = result['data'][index]['AppID']
            sub_result = get_sub_list(welink_id=welink_id, sub_type=0, sub_id=query_id)
            if sub_result.get("length") > 0:
                result['data'][index]['status'] = True
            else:
                result['data'][index]['status'] = False

    result['timeCost'] = time.time() * 1000 - start_timestamp
    result['cached'] = cached
    return {
        "msg": "ok",
        "code": 0,
        "result": result
    }


@bp.route("/count", methods=["POST"])
def http_count_recruitment():
    start_timestamp = time.time() * 1000
    error_list = []

    start_date = request.form.get("date_start")
    end_date = request.form.get("date_end")

    if start_date:
        if not re.match(re_date, start_date):
            error_list.append("Illegal param 'date_start', it should be like '2021-01-01'.")
    if end_date:
        if not re.match(re_date, end_date):
            error_list.append("Illegal param 'date_end', it should be like '2021-01-01'.")
    if len(error_list) > 0:
        return gen_error_msg(error_list, 400)

    cache_data = cache.get(f"http_count_recruitment_{start_date}_{end_date}")
    if cache_data:
        result = json.loads(cache_data)
        cached = True
    else:
        result = count_recruitment(start_date=start_date, end_date=end_date)
        if result['code'] != 0:
            return result
        result.__delitem__('code')
        cache.set(f"http_count_recruitment_{start_date}_{end_date}",
                  json.dumps(result), ex=300)
        cached = False

    result['timeCost'] = time.time() * 1000 - start_timestamp
    result['cached'] = cached
    return {
        "msg": "ok",
        "code": 0,
        "result": result
    }
