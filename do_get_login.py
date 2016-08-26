import BaseHTTPServer
import mysql_method

def do_get_login(handler):

    user_id = handler.headers['user_id']

    mysql_obj = mysql_method.MysqlObject('mysql_test', 'mysql', 'photo_share_app')
    mysql_obj.connect()
    column = 'user_name'
    table  = 'users'
    where  = 'user_id=\'{}\''.format(user_id)
    cursor, count = mysql_obj.select(column, table, where)
    user_name = ''

    if count == 0:
        body_msg = 'not found your account'
    else:
        user_name = cursor.next()[0]
        body_msg = 'found your account,user_id:{},user_name:{}'.format(user_id, user_name)
        
    # Response -- header --
    handler.send_response(200)
    handler.send_header("Content-type", "text/plain")
    handler.end_headers()
    # Response -- body --
    handler.wfile.write(body_msg)
    
    return 
