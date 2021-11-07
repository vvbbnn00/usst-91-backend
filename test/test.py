from utils.welink import *

if __name__ == '__main__':
    # print(add_calendar(welink_id="lutiancheng_659@usst", content="测试日历", start_time=(time.time() + 3600) * 1000,
    #                    end_time=(time.time() + 3601) * 1000, remind_min=10, summary="测试日历", location="测试地点"))

    # print(edit_calendar(cal_id="1636211510021i40e81368-f727-46c0-b6bb-8b4cb9367501", welink_id="lutiancheng_659@usst",
    #                     content="测试日历", start_time=(time.time() + 3600) * 1000,
    #                     end_time=(time.time() + 3601) * 1000, remind_min=10, summary="测试日历1",
    #                     location="测试地点"))

    print(delete_calendar(cal_id="1636211510021i40e81368-f727-46c0-b6bb-8b4cb9367501",
                          welink_id="lutiancheng_659@usst"))
