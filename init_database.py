import mysql_method

def create_mysql_user(user_name, password):
  mysql_obj = mysql_method.MysqlObject('root', '')
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

  create_mysql_user(user_name, password)
  create_database(user_name, password, database_name)
  create_tables(user_name, password, database_name)
  
if __name__ == '__main__':
  main()
