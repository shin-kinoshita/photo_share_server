import sys
sys.path.append('./mysql_method')
import mysql_method

operate_user_name = 'root'
operate_password  = ''

def delete_mysql_user(user_name):
  mysql_obj = mysql_method.MysqlObject(operate_user_name, operate_password)
  mysql_obj.connect()
  cur, count = mysql_obj.select('host, user', 'mysql.user', 'user=\'{}\''.format(user_name)) 
  
  for i in range(count):
    result = cur.next()
    mysql_obj_ = mysql_method.MysqlObject(operate_user_name, operate_password)
    mysql_obj_.connect()
    mysql_obj_.delete_user(result[1], result[0])

def delete_database(database_name):
  mysql_obj = mysql_method.MysqlObject(operate_user_name, operate_password)
  mysql_obj.connect()
  cur = mysql_obj.show('DATABASES', like=database_name)

  for result in cur:
    mysql_obj_ = mysql_method.MysqlObject(operate_user_name, operate_password)
    mysql_obj_.connect()
    mysql_obj_.delete_database(result[0])
  
def create_mysql_user(user_name, password):
  mysql_obj = mysql_method.MysqlObject(operate_user_name, operate_password)
  mysql_obj.connect()
  mysql_obj.create_user(user_name, password, grant_all=True)
  
def create_database(user_name, password, database_name):
  mysql_obj = mysql_method.MysqlObject(user_name, password)
  mysql_obj.connect()
  mysql_obj.create_database(database_name)

def create_tables(user_name, password, database_name):
  mysql_obj = mysql_method.MysqlObject(user_name, password)
  mysql_obj.connect()

  users_table = 'users'
  users_elements = ['user_id', 'user_name', 'event']
  users_types    = ['int', 'varchar(100)', 'varchar(100)']
  mysql_obj.create_table(database_name, users_table, users_elements, users_types)

  images_table = 'images'
  images_elements = ['image_id', 'image_name', 'user_id', 'upload_time']
  images_types    = ['int', 'varchar(100)', 'int', 'datetime']
  mysql_obj.create_table(database_name, images_table, images_elements, images_types)

  share_images_table = 'share_images'
  share_images_elements = ['image_id', 'from_user_id', 'to_user_id', 'share_start_time', 'is_shared']
  share_images_types    = ['int', 'int', 'int', 'datetime', 'varchar(10)']
  mysql_obj.create_table(database_name, share_images_table, share_images_elements, share_images_types)

  train_images_table = 'train_images'
  train_images_elements = ['image_id', 'image_name', 'user_id', 'upload_time']
  train_images_types    = ['int', 'varchar(100)', 'int', 'datetime']
  mysql_obj.create_table(database_name, train_images_table, train_images_elements, train_images_types)

def main():
  user_name = 'mysql_test'
  password = 'Mysql@2016'
  database_name = 'photo_share_app'

  delete_mysql_user(user_name)
  delete_database(database_name)
  
  create_mysql_user(user_name, password)
  create_database(user_name, password, database_name)
  create_tables(user_name, password, database_name)
  
if __name__ == '__main__':
  if len(sys.argv) >= 2:
    operate_user_name = sys.argv[1]
  if len(sys.argv) >= 3:
    operate_password= sys.argv[2]
  main()
