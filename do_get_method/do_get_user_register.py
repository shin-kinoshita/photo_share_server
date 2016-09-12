import sys
sys.path.append('../mysql_method')
import BaseHTTPServer
import mysql_method

def do_get_user_register(handler):

    param = handler.path.split('?', 1)
    if len(param) < 2:
        return

    user_name = param[1]

    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    user_id = mysql_obj.table_row_count('users')
    table_name = 'users'
    table      = '(user_id, user_name, event)'
    values     = '(\'{}\', \'{}\', NULL)'.format(user_id, user_name)
    mysql_obj.insert_into(table_name, table, values)

    # Response -- header --
    handler.send_response(200)
    handler.send_header("Content-type", "text/plain")
    handler.end_headers()
    # Response -- body --
    handler.wfile.write('message:server registered your account successfully,')
    handler.wfile.write('user_id:{},'.format(user_id))
    handler.wfile.write('user_name:{}'.format(user_name))
    
    return 
