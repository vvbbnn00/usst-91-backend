from sql import get_mssql
from utils.error import gen_error_msg
import traceback
import time


def query_meet_table(start_date=None, end_date=None,
                     kw=None, _id=None, limit=30,
                     page=0, date_order="desc"):
    """
    查询数据库并返回招聘会基础数据
    :param date_order: 日期排序参数
    :param start_date: 开始日期
    :param end_date:  结束日期
    :param kw: 查询关键词
    :param _id: 指定id查询
    :param limit: 返回数据数量限制
    :param page: 分页参数
    :return: 包装好的数据
    """
    query_list = ["FabuFlag='是'"]
    db = get_mssql()
    if page == 0:
        page = 1
    if db['code'] < 0:
        return db
    db = db['sql']
    cursor = db.cursor()
    if start_date:
        query_list.append(f"MeetStart>='{start_date} 00:00:00'")
    if end_date:
        query_list.append(f"MeetEnd<='{end_date} 23:59:59'")
    if _id:
        query_list.append(f"MeetID='{_id}'")
    if kw:
        query_list.append(f"MeetName like '%{kw}%'")

    try:
        sql = f"select [MeetID],[MeetName],[MeetAddress],[MeetStart],[MeetEnd],[AppStart],[AppEnd]" \
              f" from IJCenterOfCareer_LiXin.dbo.[MeetTable] where {' and '.join(query_list)} " \
              f"order by MeetStart {date_order} offset {(page - 1) * limit} rows fetch next {limit} rows only"
        cursor.execute(sql)
        result = cursor.fetchall()

        data = []
        for item in result:
            data.append({
                "MeetID": item[0],
                "MeetName": item[1],
                "MeetAddress": item[2],
                "MeetStart": item[3],
                "MeetEnd": item[4],
                "AppStart": item[5],
                "AppEnd": item[6]
            })
        db.close()
        return {
            "code": 0,
            "hasMore": limit == len(data),
            "next": page + 1,
            "data": data,
            "length": len(data)
        }
    except:
        db.close()
        traceback.print_exc()
        return gen_error_msg(["SQL Server Error"], 500)


def count_meet_table(start_date=None, end_date=None, kw=None):
    """
    查询数据库并返回招聘会数量
    :param start_date: 开始日期
    :param end_date:  结束日期
    :param kw: 查询关键词
    :return: 包装好的数据
    """
    search_list = ["FabuFlag='是'"]
    db = get_mssql()
    if db['code'] < 0:
        return db
    db = db['sql']
    cursor = db.cursor()
    if start_date:
        search_list.append(f"MeetStart>='{start_date} 00:00:00'")
    if end_date:
        search_list.append(f"MeetEnd<='{end_date} 23:59:59'")
    if kw:
        search_list.append(f"MeetName like '%{kw}%'")

    try:
        sql = f"select count(MeetID) from IJCenterOfCareer_LiXin.dbo.MeetTable "
        if len(search_list) > 0:
            sql += f"where {' and '.join(search_list)}"
        cursor.execute(sql)
        result = cursor.fetchval()
        db.close()
        return {
            "code": 0,
            "total": result
        }
    except:
        db.close()
        traceback.print_exc()
        return gen_error_msg(["SQL Server Error"], 500)
