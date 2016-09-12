import sys
sys.path.append('../mysql_method')
import BaseHTTPServer
import mysql_method

def do_get_event_exit(handler):

    user_id    = handler.headers['user_id']

    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    table  = 'users'
    column = 'event'
    value  = 'NULL'
    where = 'user_id = {}'.format(user_id)
    mysql_obj.update(table, column, value, where)

    # Response -- header --
    handler.send_response(200)
    handler.send_header("Content-type", "text/plain")
    handler.end_headers()
    # Response -- body --
    handler.wfile.write('message:server registered your event exit,')
    handler.wfile.write('user_id:{}'.format(user_id))
    
    return 
