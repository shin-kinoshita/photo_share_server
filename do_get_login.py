import BaseHTTPServer
import mysql_method

def do_get_login(handler):

    user_id = handler.headers['user_id']

    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    column = 'user_name, event'
    table  = 'users'
    where  = 'user_id=\'{}\''.format(user_id)
    cursor, count = mysql_obj.select(column, table, where)
    user_name = ''

    if count == 0:
        body_msg = 'message:not found your account'
    else:
        result = cursor.next()
        user_name = result[0]
        event_name = result[1] 
        if event_name == None:
            body_msg = 'message:found your account,user_id:{},user_name:{}'.format(user_id, user_name)
        else:
            body_msg = 'message:found your account,user_id:{},user_name:{},event_name:{}'.format(user_id, user_name, event_name)
        
    # Response -- header --
    handler.send_response(200)
    handler.send_header("Content-type", "text/plain")
    handler.end_headers()
    # Response -- body --
    handler.wfile.write(body_msg)
    
    return 
