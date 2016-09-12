import sys
sys.path.append('../mysql_method')
import BaseHTTPServer
import cgi
from PIL import Image
import StringIO
import mysql_method
import os

def do_post_share(handler):

    # Parse the form data posted
    form = cgi.FieldStorage(
        fp=handler.rfile, 
        headers=handler.headers,
        environ={'REQUEST_METHOD':'POST',
                 'CONTENT_TYPE':handler.headers['Content-Type'],
                 })
    image_id        = form['image_id'].value
    to_user_id_list = [int(i) for i in form['to_user_id'].value.split(',')]
    from_user_id    = handler.headers['user_id']
    
    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    for to_user_id in to_user_id_list:
        table_name = 'share_images'
        table      = '(image_id, from_user_id, to_user_id, share_start_time, is_shared)'
        values     = '({}, \'{}\', \'{}\', now(), \'false\')'.format(image_id, from_user_id, to_user_id)
        mysql_obj.insert_into(table_name, table, values)
    mysql_obj.disconnect()
    
    # Response -- header --
    handler.send_response(200)
    handler.send_header("Content-type", "text/plain")
    handler.end_headers()
    # Response -- body --
    handler.wfile.write('message:server shared image,')
    handler.wfile.write('image_id:{}'.format(image_id))

    return

def do_post_error(handler):
    
    return

