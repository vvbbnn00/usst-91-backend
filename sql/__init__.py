import sql.connector
import config
from utils.error import gen_error_msg
import redis

db_config = config.sqlConfig
db = connector.MsSql(server=db_config['server'], database=db_config['database'],
                     username=db_config['username'], password=db_config['password'])


def get_mssql():
    try:
        sql = connector.MsSql(server=db_config['server'], database=db_config['database'],
                              username=db_config['username'], password=db_config['password'])
        return {
            "code": 0,
            "sql": sql
        }
    except:
        return gen_error_msg(["SQL Connection Error."], 500)


cache = redis.StrictRedis(host=config.cacheConfig['host'], port=config.cacheConfig['port'],
                          db=config.cacheConfig['db'], password=config.cacheConfig['password'])

