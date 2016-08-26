import BaseHTTPServer
import mysql_method

def get_user_info(mac_addr):
    mysql_obj = mysql_method.MysqlObject('mysql_test', 'mysql', 'photo_share_app')
    mysql_obj.connect()

    column = 'user_id, user_name'
    table  = 'users'
    where  = 'mac_addr=\'{}\''.format(mac_addr)
    result = mysql_obj.select(column, table, where)
    try:
        (user_id, user_name) = result.next()
    except StopIteration:
        (user_id, user_name) = (None, None)
        
    return user_id, user_name
