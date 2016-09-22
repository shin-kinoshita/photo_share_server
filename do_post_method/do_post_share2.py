import sys
sys.path.append('../mysql_method')
sys.path.append('../face_recognition')
import BaseHTTPServer
import cgi
from PIL import Image
import StringIO
import mysql_method
import detect_to_user
from detect_to_user import detect_to_user
import os

def do_post_share2(handler, images_dir, train_images_dir):

    user_id = handler.headers['user_id']

    # Parse the form data posted
    form = cgi.FieldStorage(
        fp=handler.rfile, 
        headers=handler.headers,
        environ={'REQUEST_METHOD':'POST',
                 'CONTENT_TYPE':handler.headers['Content-Type'],
                 })

    image_name, image = _extract_image(form)
    num_images = len(os.listdir(images_dir))
    image_id = num_images + 1

    to_user_id_list = detect_to_user(user_id, image, train_images_dir)
    if to_user_id_list == None:
        print 'Error'
        return

    to_user_id_str = ''
    for to_user_id in to_user_id_list:
        to_user_id_str += str(to_user_id) + ','
    to_user_id_str = to_user_id_str[:-1]

    _save_image(image, image_name, image_id, images_dir)

    _save_image_info(image, image_id, image_name, user_id)

    _save_share_image_info(image_id, user_id, to_user_id_list)
    
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

def _save_image(image, image_name, image_id, images_dir):
    image_ext = image_name.split('.')[1]
    image_save_path = images_dir + '/' + str(image_id) + '.' + image_ext
    image.save(image_save_path)

def _save_image_info(image, image_id, image_name, user_id):
    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    table_name = 'images'
    table      = '(image_id, image_name, user_id, upload_time)'
    values     = '({}, \'{}\', {}, now())'.format(image_id, image_name, user_id)
    mysql_obj.insert_into(table_name, table, values)
    mysql_obj.disconnect()

def _save_share_image_info(image_id, user_id, to_user_id_list):
    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    for to_user_id in to_user_id_list:
        table_name = 'share_images'
        table      = '(image_id, from_user_id, to_user_id, share_start_time, is_shared)'
        values     = '({}, \'{}\', \'{}\', now(), \'false\')'.format(image_id, user_id, to_user_id)
        mysql_obj.insert_into(table_name, table, values)
    mysql_obj.disconnect()

def do_post_error(handler):
    
    return

