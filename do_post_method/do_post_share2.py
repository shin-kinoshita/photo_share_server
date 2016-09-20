import sys
sys.path.append('../mysql_method')
import BaseHTTPServer
import cgi
from PIL import Image
import StringIO
import mysql_method
import os

def do_post_share2(handler, image_save_dir):

    user_id = handler.headers['user_id']

    # Parse the form data posted
    form = cgi.FieldStorage(
        fp=handler.rfile, 
        headers=handler.headers,
        environ={'REQUEST_METHOD':'POST',
                 'CONTENT_TYPE':handler.headers['Content-Type'],
                 })
    image_name, image = _extract_image(form)
    
    to_user_id_list = [int(i) for i in form['to_user_id'].value.split(',')]

    image_ext = image_name.split('.')[1]
    num_save_dir = len(os.listdir(image_save_dir))
    image_id = num_save_dir

    image_save_path = image_save_dir + '/' + str(image_id) + '.' + image_ext
    image.save(image_save_path)
    
    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    table_name = 'images'
    table      = '(image_id, image_name, user_id, upload_time)'
    values     = '({}, \'{}\', {}, now())'.format(image_id, image_name, user_id)
    mysql_obj.insert_into(table_name, table, values)
    mysql_obj.disconnect()

    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    to_user_id_str = ''
    for to_user_id in to_user_id_list:
        to_user_id_str += str(to_user_id) + ','
        table_name = 'share_images'
        table      = '(image_id, from_user_id, to_user_id, share_start_time, is_shared)'
        values     = '({}, \'{}\', \'{}\', now(), \'false\')'.format(image_id, user_id, to_user_id)
        mysql_obj.insert_into(table_name, table, values)
    mysql_obj.disconnect()
    to_user_id_str = to_user_id_str[:-1]

    # Response -- header --
    handler.send_response(200)
    handler.send_header("Content-type", "text/plain")
    handler.end_headers()
    # Response -- body --
    handler.wfile.write('message:server saved and shared your image,')
    handler.wfile.write('image_id:{},'.format(image_id))
    handler.wfile.write('image_name:{}'.format(image_name))
    handler.wfile.write('to_user_id:{}'.format(to_user_id_str))

    return

def _extract_image(cgi_form):

    image_key = 'image'

    name = ""
    image_item = None
    if image_key in cgi_form == False:
        return None, None

    name = cgi_form[image_key].filename
    image_item = cgi_form[image_key]

    if name == "" or image_item == None:
        return None, None

    raw_data = image_item.file.read()
    image = Image.open(StringIO.StringIO(raw_data))

    return name, image

def do_post_error(handler):
    
    return

