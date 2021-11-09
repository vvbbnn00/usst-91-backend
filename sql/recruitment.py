from sql import get_mssql
from utils.error import gen_error_msg
import traceback
import time


def query_recruitment(start_date=None, end_date=None,
                      kw=None, _id=None, limit=30, page=0,
                      date_order="desc"):
    """
    查询数据库并返回宣讲会基础数据
    :param date_order: 日期排序 asc 从低到高 desc 从高到低
    :param start_date: 开始日期
    :param end_date:  结束日期
    :param kw: 查询关键词
    :param _id: 指定id查询
    :param limit: 返回数据数量限制
    :param page: 分页查询
    :return: 包装好的数据
    """

    query_list = ["CheckFlag='是'"]
    if page == 0:
        page = 1
    db = get_mssql()
    if db['code'] < 0:
        return db
    db = db['sql']
    cursor = db.cursor()
    if start_date:
        query_list.append(f"ScheduledDate>='{start_date}'")
    if end_date:
        query_list.append(f"ScheduledDate<='{end_date}'")
    if _id:
        query_list.append(f"AppID='{_id}'")
    if kw:
        query_list.append(f"EntName like '%{kw}%'")

    try:
        sql = f"select [AppID],[SequenceNumber],[EntName]," \
              f"[HostVenue],[ScheduledDate],[ScheduledDateS]," \
              f"[ScheduledDateE] from IJCenterOfCareer_LiXin.dbo.CampusRecruitment " \
              f"where {' and '.join(query_list)} " \
              f"order by ScheduledDate {date_order},ScheduledDateS {date_order} " \
              f"offset {(page - 1) * limit} rows fetch next {limit} rows only"
        cursor.execute(sql)
        result = cursor.fetchall()

        data = []
        for item in result:
            data.append({
                "AppID": item[0],
                "SequenceNumber": item[1],
                "EntName": item[2],
                "HostVenue": item[3],
                "ScheduledDate": item[4],
                "ScheduledDateS": item[5],
                "ScheduledDateE": item[6]
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
        traceback.print_exc()
        db.close()
        return gen_error_msg(["SQL Server Error"], 500)


def count_recruitment(start_date=None, end_date=None, kw=None):
    """
    查询数据库并返回宣讲会数量
    :param start_date: 开始日期
    :param end_date:  结束日期
    :param kw: 查询关键词
    :return: 包装好的数据
    """
    search_list = ["CheckFlag='是'"]
    db = get_mssql()
    if db['code'] < 0:
        return db
    db = db['sql']
    cursor = db.cursor()
    if start_date:
        search_list.append(f"ScheduledDate>='{start_date}'")
    if end_date:
        search_list.append(f"ScheduledDate<='{end_date}'")
    if kw:
        search_list.append(f"EntName like '%{kw}%'")

    try:
        sql = f"select count(AppID) from IJCenterOfCareer_LiXin.dbo.CampusRecruitment "
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
        traceback.print_exc()
        db.close()
        return gen_error_msg(["SQL Server Error"], 500)
