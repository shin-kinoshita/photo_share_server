import BaseHTTPServer
import mysql_method

def do_get_event_register(handler):

    param = handler.path.split('?', 1)
    if len(param) < 2:
        return

    event_name = param[1]
    user_id    = handler.headers['user_id']

    mysql_obj = mysql_method.MysqlObject('mysql_test', 'mysql', 'photo_share_app')
    mysql_obj.connect()
    table = 'users'
    column = 'event'
    value = '\'{}\''.format(event_name)
    where = 'user_id = {}'.format(user_id)
    mysql_obj.update(table, column, value, where)

    # Response -- header --
    handler.send_response(200)
    handler.send_header("Content-type", "text/plain")
    handler.end_headers()
    # Response -- body --
    handler.wfile.write('message:server registered event to your account,')
    handler.wfile.write('user_id:{},'.format(user_id))
    handler.wfile.write('event_name:{}'.format(event_name))
    
    return 
