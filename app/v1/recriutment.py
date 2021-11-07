from flask import *
from sql.recruitment import *
import re

re_date = r"\d{4}-\d{2}-\d{2}"

bp = Blueprint('v1_recruitment', __name__, url_prefix='/recruit')


@bp.route("/query", methods=["POST"])
def http_query_recruitment():
    error_list = []
    start_date = request.form.get("date_start")
    end_date = request.form.get("date_end")
    if not start_date or not end_date:
        error_list.append("Param 'date_start' and 'date_end' is required.")
        return gen_error_msg(error_list, 400)

    if not re.match(re_date, start_date):
        error_list.append("Illegal param 'date_start', it should be like '2021-01-01'.")
    if not re.match(re_date, end_date):
        error_list.append("Illegal param 'date_end', it should be like '2021-01-01'.")

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

    result = query_recruitment(start_date=start_date, end_date=end_date, limit=limit, q_from=q_from)

    if result['code'] != 0:
        return result

    result.__delitem__('code')

    return {
        "msg": "ok",
        "code": 0,
        "result": result
    }


@bp.route("/count", methods=["POST"])
def http_count_recruitment():
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

    result = count_recruitment(start_date=start_date, end_date=end_date)
    if result['code'] != 0:
        return result
    result.__delitem__('code')

    return {
        "msg": "ok",
        "code": 0,
        "result": result
    }
