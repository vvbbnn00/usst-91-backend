def gen_error_msg(error_list, err_code):
    err_str = ','.join(error_list)
    return {
        "code": err_code,
        "msg": err_str
    }
