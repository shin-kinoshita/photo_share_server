import sys
sys.path.append('../mysql_method')
import BaseHTTPServer
import mysql_method

def do_get_event_info(handler):

    param = handler.path.split('?', 1)
    if len(param) < 2:
        return

    event_name = param[1]
    user_id    = handler.headers['user_id']

    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    column = 'user_id, user_name'
    table = 'users'
    where = 'event = \'{}\''.format(event_name)
    cursor, count = mysql_obj.select(column, table, where)

    user_id_str = ''
    user_name_str = ''
    for i in range(count):
        result = cursor.next()
        user_id_str += str(result[0]) + '_'
        user_name_str += str(result[1]) + '_'
    user_id_str = user_id_str.rsplit('_', 1)[0]
    user_name_str = user_name_str.rsplit('_', 1)[0]

    # Response -- header --
    handler.send_response(200)
    handler.send_header("Content-type", "text/plain")
    handler.end_headers()
    # Response -- body --
    handler.wfile.write('message:user_id_list registered to event is shown,')
    handler.wfile.write('user_id_list:{},'.format(user_id_str))
    handler.wfile.write('user_name_list:{}'.format(user_name_str))
    
    return 

