import BaseHTTPServer
import mysql_method

def do_get_event_info(handler):

    param = handler.path.split('?', 1)
    if len(param) < 2:
        return

    event_name = param[1]
    user_id    = handler.headers['user_id']

    mysql_obj = mysql_method.MysqlObject('mysql_test', 'mysql', 'photo_share_app')
    mysql_obj.connect()
    column = 'user_id'
    table = 'users'
    where = 'event = \'{}\''.format(event_name)
    cursor, count = mysql_obj.select(column, table, where)

    user_id_str = ""
    for i in range(count):
        user_id_str += str(cursor.next()[0]) + ','
    user_id_str = user_id_str.rsplit(',', 1)[0]

    # Response -- header --
    handler.send_response(200)
    handler.send_header("Content-type", "text/plain")
    handler.end_headers()
    # Response -- body --
    handler.wfile.write('message:user_id_list registered to event is shown,')
    handler.wfile.write('user_id_list:{}'.format(user_id_str))
    
    return 
