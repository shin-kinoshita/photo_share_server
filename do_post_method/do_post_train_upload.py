import sys
sys.path.append('../mysql_method')
import BaseHTTPServer
import cgi
from PIL import Image
import StringIO
import mysql_method
import os

def do_post_train_upload(handler):

    image_save_dir = '../train_images'

    user_id = handler.headers['user_id']

    # Parse the form data posted
    form = cgi.FieldStorage(
        fp=handler.rfile, 
        headers=handler.headers,
        environ={'REQUEST_METHOD':'POST',
                 'CONTENT_TYPE':handler.headers['Content-Type'],
                 })
    image_name, image = _extract_image(form)
    #face_rec_list     = _extract_rec_list(form)
    #face_name_list    = extract_name_list(image, face_rec_list)

    image_ext = image_name.split('.')[1]
    num_save_dir = len(os.listdir(image_save_dir))
    image_id = num_save_dir + 1

    image_save_path = image_save_dir + '/' + str(image_id) + '.' + image_ext
    image.save(image_save_path)
    
    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    table_name = 'train_images'
    table      = '(image_id, image_name, user_id, upload_time)'
    values     = '({}, \'{}\', {}, now())'.format(image_id, image_name, user_id)
    mysql_obj.insert_into(table_name, table, values)
    mysql_obj.disconnect()
    
    # Response -- header --
    handler.send_response(200)
    handler.send_header("Content-type", "text/plain")
    handler.end_headers()
    # Response -- body --
    handler.wfile.write('message:server got and saved your train image,')
    handler.wfile.write('image_id:{},'.format(image_id))
    handler.wfile.write('image_name:{}'.format(image_name))

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

def _extract_rec_list(cgi_form):

    rec_key = 'face_rec'

    if image_key in cgi_form == False:
        return None
    
    num_list = cgi_form[rec_key].value.split(',')
    num_len = len(num_list)
    rec_list = []
    for i in range(0, num_len, 4):
        point1 = (int(num_list[i]),   int(num_list[i+1]))
        point2 = (int(num_list[i+2]), int(num_list[i+3]))
        rec_list.append([point1, point2])
    return rec_list

def _extract_name_list(cgi_form):

    name_list_key = "name_list"
    
    if name_list_key in cgi_form == False:
        return None, None

    name_list = cgi_form[name_list_key].value.split(',')

    return name_list

def do_post_error(handler):
    
    return

