import sys
sys.path.append('./do_get_method')
sys.path.append('./do_post_method')
sys.path.append('./mysql_method')
import BaseHTTPServer
import time
import do_get_login
import do_get_user_register
import do_get_event_register
import do_get_event_exit
import do_get_event_info
import do_get_download
import do_post_upload
import do_post_train_upload
import do_post_share
import do_post_share2
from do_get_login import do_get_login
from do_get_user_register import do_get_user_register
from do_get_event_register import do_get_event_register
from do_get_event_exit import do_get_event_exit
from do_get_event_info import do_get_event_info
from do_get_download import do_get_download
from do_post_upload import do_post_upload
from do_post_train_upload import do_post_train_upload
from do_post_share import do_post_share
from do_post_share2 import do_post_share2

HOST_NAME = '192.168.1.150' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000      # Maybe set this to 9000.

image_save_dir = './images'
train_image_save_dir = './train_images'

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):

        if 'mode' in self.headers == False:
            do_error(self, 'mode header not fount')
            return
        mode = self.headers['mode']

        if mode == 'login':
            do_get_login(self)
        elif mode == 'user_register':
            do_get_user_register(self)
        elif mode == 'event_register':
            do_get_event_register(self)
        elif mode == 'event_exit':
            do_get_event_exit(self)
        elif mode == 'event_info':
            do_get_event_info(self)
        elif mode == 'download':
            do_get_download(self, image_save_dir)
        else :
            do_error(self, 'mode not hit')

        return

    def do_POST(self):

        if 'mode' in self.headers == False:
            do_error(self, 'mode header not fount')
            return
        mode = self.headers['mode']

        if mode == 'train_upload':
            do_post_train_upload(self, train_image_save_dir)
        elif mode == 'share2':
            do_post_share2(self, image_save_dir)
        else :
            do_error(self, 'mode not hit')
            
        return

def do_error(handler, msg):
    print msg
    return

def main():
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

if __name__ == '__main__':
    main()
