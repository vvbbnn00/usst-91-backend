def gen_error_msg(error_list, err_code):
    err_str = "Errors occurred when dealing with the request:" + ','.join(error_list)
    return {
        "code": err_code,
        "msg": err_str
    }
