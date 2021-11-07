import datetime
import time
import traceback
from sql.recruitment import query_recruitment
from sql.meet_table import query_meet_table
from utils.welink import delete_calendar, add_calendar, edit_calendar
from config import mysqlConfig
import pymysql


def gen_meet_content_str(meet_data):
    return f"""就业招聘会
主题：{meet_data["MeetName"]}
地点：{meet_data["MeetAddress"]}
报名开始时间：{meet_data["AppStart"].strftime("%Y-%m-%d %H:%M:%S")}
报名结束时间：{meet_data["AppEnd"].strftime("%Y-%m-%d %H:%M:%S")}
招聘会开始时间：{meet_data["MeetStart"].strftime("%Y-%m-%d %H:%M:%S")}
招聘会结束时间：{meet_data["MeetEnd"].strftime("%Y-%m-%d %H:%M:%S")}
（本日程由就业日历自动创建）
"""


def gen_recruit_content_str(rec_data):
    return f"""就业宣讲会
企业：{rec_data["EntName"]}
地点：{rec_data["HostVenue"]}
开始时间：{rec_data["ScheduledDate"].strftime("%Y-%m-%d")} {rec_data["ScheduledDateS"]}
结束时间：{rec_data["ScheduledDate"].strftime("%Y-%m-%d")} {rec_data["ScheduledDateE"]}
（本日程由就业日历自动创建）
"""


def calc_time_delta(time):
    hour = int(str(time).split(":")[0])
    minute = int(str(time).split(":")[0])
    return (hour * 3600 + minute * 60) * 1000


def get_db():
    try:
        db = pymysql.connect(host=mysqlConfig['server'], user=mysqlConfig['username'],
                             password=mysqlConfig['password'], database=mysqlConfig['database'],
                             port=int(mysqlConfig['port']))
        return {
            'code': 0,
            'sql': db
        }
    except:
        traceback.print_exc()
        return {
            'code': 500,
            'msg': 'Sql Server Connection Error.'
        }


def get_meet_detail(meet_id):
    start_timestamp = time.time()
    db = get_db()
    if db['code'] != 0:
        return db
    db = db['sql']
    cursor = db.cursor()
    sql = f"select MeetID,MeetName,MeetAddress,MeetStart,MeetEnd,AppStart,AppEnd from usst91.meet_list " \
          f"where MeetID='{meet_id}'"
    cursor.execute(sql)
    result = cursor.fetchone()
    db.close()
    if not result:
        return {
            'code': 400,
            'msg': 'Meet not found.'
        }
    return {
        'timeCost': (start_timestamp - time.time()) * 1000,
        'code': 0,
        'MeetID': result[0],
        'MeetName': result[1],
        'MeetAddress': result[2],
        'MeetStart': result[3],
        'MeetEnd': result[4],
        'AppStart': result[5],
        'AppEnd': result[6],
    }


def update_meet_detail(meet_id, MeetName=None, MeetAddress=None, MeetStart=None,
                       MeetEnd=None, AppStart=None, AppEnd=None):
    db = get_db()
    if db['code'] != 0:
        return db
    db = db['sql']
    cursor = db.cursor()
    sql = f"replace into usst91.meet_list (MeetID,MeetName,MeetAddress,MeetStart,MeetEnd,AppStart,AppEnd) values" \
          f" ('{meet_id}','{MeetName}','{MeetAddress}','{MeetStart}','{MeetEnd}','{AppStart}','{AppEnd}')"
    cursor.execute(sql)
    db.commit()
    db.close()
    return {
        'code': 0
    }


def get_recruit_detail(recruit_id):
    start_timestamp = time.time()
    db = get_db()
    if db['code'] != 0:
        return db
    db = db['sql']
    cursor = db.cursor()
    sql = f"select AppID,SequenceNumber,EntName,HostVenue,ScheduledDate,ScheduledDateS,ScheduledDateE" \
          f" from usst91.recruitment_list " \
          f"where AppID='{recruit_id}'"
    cursor.execute(sql)
    result = cursor.fetchone()
    db.close()
    if not result:
        return {
            'code': 400,
            'msg': 'Recruitment not found.'
        }
    return {
        'timeCost': (start_timestamp - time.time()) * 1000,
        'code': 0,
        'AppID': result[0],
        'SequenceNumber': result[1],
        'EntName': result[2],
        'HostVenue': result[3],
        'ScheduledDate': result[4],
        'ScheduledDateS': result[5],
        'ScheduledDateE': result[6],
    }


def update_recruit_detail(recruit_id, SequenceNumber=None, EntName=None, HostVenue=None,
                          ScheduledDate=None, ScheduledDateS=None, ScheduledDateE=None):
    db = get_db()
    if db['code'] != 0:
        return db
    db = db['sql']
    cursor = db.cursor()
    sql = f"replace into usst91.recruitment_list " \
          f"(AppID,SequenceNumber,EntName,HostVenue,ScheduledDate,ScheduledDateS,ScheduledDateE) values" \
          f" ('{recruit_id}','{SequenceNumber}','{EntName}','{HostVenue}','{ScheduledDate}'," \
          f"'{ScheduledDateS}','{ScheduledDateE}')"
    cursor.execute(sql)
    db.commit()
    db.close()
    return {
        'code': 0
    }


def get_sub_list(welink_id=None, sub_type=None, sub_id=None, limit=30, q_from=None):
    start_timestamp = time.time()
    if limit > 500:
        limit = 500
    db = get_db()
    if db['code'] != 0:
        return db
    db = db['sql']
    cursor = db.cursor()
    search_list = ["status=0"]
    if welink_id:
        search_list.append(f"welink_id='{welink_id}'")
    if sub_id:
        search_list.append(f"sub_id='{sub_id}'")
    if sub_type:
        search_list.append(f"sub_type={sub_type}")
    if q_from:
        search_list.append(f"Id<{q_from}")
    sql = f"select id,welink_id,sub_type,sub_id,calendar_id from usst91.subscription_list "
    if len(search_list) > 0:
        sql += f"where ({') and ('.join(search_list)})"
    sql += f"ORDER BY Id DESC limit {limit}"
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    data = []
    for item in result:
        data.append({
            'id': item[0],
            'welink_id': item[1],
            'sub_type': item[2],
            'sub_id': item[3],
            'cal_id': item[4]
        })
    return {
        'code': 0,
        'msg': 'ok',
        'data': data,
        'timeCost': (time.time() - start_timestamp) * 1000,
        'length': len(data),
        'next': '0' if len(data) == 0 else data[-1]['id'],
        'hasMore': len(data) == limit
    }


def delete_sub(welink_id=None, sub_type=None, sub_id=None):
    db = get_db()
    if db['code'] != 0:
        return db
    db = db['sql']
    cursor = db.cursor()
    sql = f"select calendar_id from usst91.subscription_list where " \
          f"welink_id='{welink_id}' and sub_type={sub_type} and sub_id='{sub_id}'and status=0"
    cursor.execute(sql)
    result = cursor.fetchone()
    if not result:
        return {
            'code': 400,
            'msg': 'Subscription not found.'
        }
    cal_id = result[0]
    result = delete_calendar(cal_id, welink_id)
    if result['code'] != 0:
        return result
    sql = f"update usst91.subscription_list set status=1 where " \
          f"welink_id='{welink_id}' and sub_type={sub_type} and sub_id='{sub_id}' and status=0"
    cursor.execute(sql)
    db.commit()
    db.close()
    return {
        'code': 0,
        'msg': 'ok'
    }


def create_sub_item(welink_id, sub_type, sub_id):
    db = get_db()
    if db['code'] != 0:
        return db
    db = db['sql']
    cursor = db.cursor()
    summary = ""
    content = ""
    location = ""
    start_time = 0
    end_time = 0

    if get_sub_list(welink_id=welink_id, sub_type=sub_type, sub_id=sub_id)['length'] > 0:
        db.close()
        return {
            'code': 400,
            'msg': 'You have already subscribed this event.'
        }

    if sub_type == 0:  # 宣讲会
        rec_data = query_recruitment(_id=sub_id)
        if rec_data['length'] == 0:
            db.close()
            return {
                'code': 400,
                'msg': 'Recruitment Not Found.'
            }
        rec_data = rec_data['data'][0]
        summary = "[宣讲会]" + rec_data["EntName"]
        content = gen_recruit_content_str(rec_data)
        location = rec_data["HostVenue"]
        start_time = int(rec_data["ScheduledDate"].timestamp() * 1000) + calc_time_delta(rec_data["ScheduledDateS"])
        end_time = int(rec_data["ScheduledDate"].timestamp() * 1000) + calc_time_delta(rec_data["ScheduledDateE"])
        if get_recruit_detail(recruit_id=sub_id)['code'] != 0:
            update_recruit_detail(recruit_id=sub_id,
                                  SequenceNumber=rec_data["SequenceNumber"], EntName=rec_data["EntName"],
                                  HostVenue=rec_data["HostVenue"],
                                  ScheduledDate=rec_data["ScheduledDate"].strftime("%Y-%m-%d"),
                                  ScheduledDateS=rec_data["ScheduledDateS"],
                                  ScheduledDateE=rec_data["ScheduledDateE"])
    elif sub_type == 1:  # 招聘会
        meet_data = query_meet_table(_id=sub_id)
        if meet_data['length'] == 0:
            db.close()
            return {
                'code': 400,
                'msg': 'Meet Not Found.'
            }
        meet_data = meet_data['data'][0]
        summary = "[招聘会]" + meet_data["MeetName"]
        content = gen_meet_content_str(meet_data)
        location = meet_data["MeetAddress"]
        start_time = int(meet_data["MeetStart"].timestamp() * 1000)
        end_time = int(meet_data["MeetEnd"].timestamp() * 1000)
        if get_meet_detail(meet_id=sub_id)['code'] != 0:
            update_meet_detail(meet_id=sub_id,
                               MeetName=meet_data["MeetName"], MeetAddress=meet_data["MeetAddress"],
                               MeetStart=meet_data["MeetStart"].strftime("%Y-%m-%d %H:%M:%S"),
                               MeetEnd=meet_data["MeetEnd"].strftime("%Y-%m-%d %H:%M:%S"),
                               AppStart=meet_data["AppStart"].strftime("%Y-%m-%d %H:%M:%S"),
                               AppEnd=meet_data["AppEnd"].strftime("%Y-%m-%d %H:%M:%S"))
    cal_id = add_calendar(welink_id=welink_id, summary=summary, content=content, location=location,
                          start_time=start_time, end_time=end_time)
    if cal_id['code'] != 0:
        db.close()
        return cal_id
    cal_id = cal_id['cal_id']
    sql = f"insert into usst91.subscription_list (welink_id, sub_type, sub_id, status, calendar_id) values " \
          f"('{welink_id}', {sub_type}, '{sub_id}', 0, '{cal_id}')"
    cursor.execute(sql)

    db.commit()
    db.close()
    return {
        'code': 0,
        'msg': 'ok'
    }


def update_data():
    print(f"--------开始刷新数据：{datetime.datetime.now()}--------")
    result = get_sub_list(limit=500)
    data = result['data']
    while result['hasMore']:
        result = get_sub_list(limit=500, q_from=result['next'])
        data += result['data']
    update_meet_list = []
    update_recruit_list = []
    meet_user = {}
    recruit_user = {}
    for item in data:
        if item['sub_type'] == 0:
            update_recruit_list.append(item['sub_id'])
            if recruit_user.__contains__(item['sub_id']):
                recruit_user[item['sub_id']].append({'cal_id': item["cal_id"], 'welink_id': item['welink_id']})
            else:
                recruit_user[item['sub_id']] = [{'cal_id': item["cal_id"], 'welink_id': item['welink_id']}]
        elif item['sub_type'] == 1:
            if meet_user.__contains__(item['sub_id']):
                meet_user[item['sub_id']].append({'cal_id': item["cal_id"], 'welink_id': item['welink_id']})
            else:
                meet_user[item['sub_id']] = [{'cal_id': item["cal_id"], 'welink_id': item['welink_id']}]
            update_meet_list.append(item['sub_id'])
    update_meet_list = set(update_meet_list)
    update_recruit_list = set(update_recruit_list)

    for meet in update_meet_list:
        meet_data = get_meet_detail(meet)
        if meet_data['code'] != 0:
            continue
        new_meet_data = query_meet_table(_id=meet)
        if new_meet_data['length'] == 0:
            continue
        new_meet_data = new_meet_data['data'][0]
        if meet_data["MeetName"] != new_meet_data["MeetName"] or \
                meet_data["MeetAddress"] != new_meet_data["MeetAddress"] or \
                meet_data["MeetStart"] != new_meet_data["MeetStart"].strftime("%Y-%m-%d %H:%M:%S") or \
                meet_data["MeetEnd"] != new_meet_data["MeetEnd"].strftime("%Y-%m-%d %H:%M:%S") or \
                meet_data["AppStart"] != new_meet_data["AppStart"].strftime("%Y-%m-%d %H:%M:%S") or \
                meet_data["AppEnd"] != new_meet_data["AppEnd"].strftime("%Y-%m-%d %H:%M:%S"):
            print(f"招聘会 {meet} 有更新")

            content = gen_meet_content_str(new_meet_data)
            start_time = int(new_meet_data["MeetStart"].timestamp() * 1000)
            end_time = int(new_meet_data["MeetEnd"].timestamp() * 1000)
            location = new_meet_data["MeetAddress"]
            summary = "[招聘会]" + new_meet_data["MeetName"]

            for user in meet_user[meet]:
                edit_calendar(welink_id=user['welink_id'], cal_id=user['cal_id'],
                              content=content,
                              start_time=start_time,
                              end_time=end_time,
                              location=location,
                              summary=summary)

            update_meet_detail(meet_id=meet,
                               MeetName=new_meet_data["MeetName"],
                               MeetAddress=new_meet_data["MeetAddress"],
                               MeetStart=new_meet_data["MeetStart"].strftime("%Y-%m-%d %H:%M:%S"),
                               MeetEnd=new_meet_data["MeetEnd"].strftime("%Y-%m-%d %H:%M:%S"),
                               AppStart=new_meet_data["AppStart"].strftime("%Y-%m-%d %H:%M:%S"),
                               AppEnd=new_meet_data["AppEnd"].strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print(f"招聘会 {meet} 已是最新")

    for recruit in update_recruit_list:
        recruit_data = get_recruit_detail(recruit)
        if recruit_data['code'] != 0:
            continue
        new_recruit_data = query_recruitment(_id=recruit)
        if new_recruit_data['length'] == 0:
            continue
        new_recruit_data = new_recruit_data['data'][0]
        if recruit_data["SequenceNumber"] != new_recruit_data["SequenceNumber"] or \
                recruit_data["EntName"] != new_recruit_data["EntName"] or \
                recruit_data["HostVenue"] != new_recruit_data["HostVenue"] or \
                recruit_data["ScheduledDate"] != new_recruit_data["ScheduledDate"].strftime("%Y-%m-%d") or \
                recruit_data["ScheduledDateS"] != new_recruit_data["ScheduledDateS"] or \
                recruit_data["ScheduledDateE"] != new_recruit_data["ScheduledDateE"]:
            print(f"宣讲会 {recruit} 有更新")

            content = gen_recruit_content_str(new_recruit_data)
            summary = "[宣讲会]" + new_recruit_data["EntName"]
            location = new_recruit_data["HostVenue"]
            start_time = int(new_recruit_data["ScheduledDate"].timestamp() * 1000) + calc_time_delta(
                new_recruit_data["ScheduledDateS"])
            end_time = int(new_recruit_data["ScheduledDate"].timestamp() * 1000) + calc_time_delta(
                new_recruit_data["ScheduledDateE"])

            for user in recruit_user[recruit]:
                edit_calendar(welink_id=user['welink_id'], cal_id=user['cal_id'],
                              content=content,
                              start_time=start_time,
                              end_time=end_time,
                              location=location,
                              summary=summary)

            update_recruit_detail(recruit_id=recruit,
                                  SequenceNumber=new_recruit_data["SequenceNumber"],
                                  EntName=new_recruit_data["EntName"],
                                  HostVenue=new_recruit_data["HostVenue"],
                                  ScheduledDate=new_recruit_data["ScheduledDate"].strftime("%Y-%m-%d"),
                                  ScheduledDateS=new_recruit_data["ScheduledDateS"],
                                  ScheduledDateE=new_recruit_data["ScheduledDateE"])
        else:
            print(f"宣讲会 {recruit} 已是最新")
    print(f"--------数据刷新结束：{datetime.datetime.now()}--------")