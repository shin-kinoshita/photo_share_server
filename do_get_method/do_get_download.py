import sys
sys.path.append('../mysql_method')
import BaseHTTPServer
import mysql_method
from PIL import Image
import StringIO

def do_get_download(handler):

    user_id = handler.headers['user_id']

    image_id, count = select_download_image(user_id)

    if image_id == None:
        # Response -- header --
        handler.send_response(200)
        handler.send_header("remained_image_count", "no image to return")
        handler.end_headers()
        return 

    image_name, f_image = import_image_from_id(image_id)
    image_ext = image_name.split('.')[1]

    update_is_shared(image_id, user_id)

    # For testing, false will be set to all is_shared property
    if count - 1 <= 0:
        update_is_shared_false(user_id)

    # Response -- header --
    handler.send_response(200)
    handler.send_header("Content-type", "image/" + image_ext)
    handler.send_header("remained_image_count", str(count - 1))
    handler.send_header("image_name", image_name)
    handler.end_headers()
    # Response -- body --
    handler.wfile.write(f_image.read())
    
    return 

def select_download_image(to_user_id):
    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    column = 'image_id'
    table = 'share_images'
    where = '(to_user_id = {} AND is_shared = \'false\')'.format(to_user_id)
    cursor, count = mysql_obj.select(column, table, where)

    if count <= 0:
        return None, count

    image_id = cursor.next()[0]
    #mysql_obj.disconnect()
    return image_id, count

def import_image_from_id(image_id):
    image_save_dir = '../images'
    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    column = 'image_name'
    table  = 'images'
    where  = 'image_id = {}'.format(image_id)
    cursor, _ = mysql_obj.select(column, table, where)
    image_name = cursor.next()[0]
    ext = image_name.split('.')[1]

    f_image = open(image_save_dir + '/' + str(image_id) + '.' + ext, 'rb')
    return image_name, f_image

def update_is_shared(image_id, to_user_id):
    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    table = 'share_images'
    column = 'is_shared'
    value  = '\'true\''
    where  = 'image_id = {} AND to_user_id = {}'.format(image_id, to_user_id)
    mysql_obj.update(table, column, value, where)

def update_is_shared_false(to_user_id):
    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    table = 'share_images'
    column = 'is_shared'
    value  = '\'false\''
    where  = 'to_user_id = {}'.format(to_user_id)
    mysql_obj.update(table, column, value, where)

