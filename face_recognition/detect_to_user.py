# -*- coding:utf-8 -*-
import sys
sys.path.append('../mysql_method')
import os
import numpy as np
import cv2
import random
import mysql_method
import face_train_transfer
from face_train_transfer import features_generator
from sklearn import svm
from PIL import Image

abs_file_path = os.path.abspath(__file__)
MODEL_PATH = os.path.dirname(abs_file_path) + '/tmp/face_model.ckpt'
SIZE = 56, 56

def detect_to_user(user_id, image, train_images_dir):
    face_image_list = _extract_face_images(image)
    print len(face_image_list)
    to_user_id_list = _get_to_user_id(user_id)
    if to_user_id_list == None:
        return None
    classifier = _generate_classifier(to_user_id_list, train_images_dir)
    result_id_list = _classify_face(classifier, face_image_list)

    return result_id_list

def _extract_face_images(image):
    cascade_path = "/usr/local/Cellar/opencv3/3.1.0_4/share/OpenCV/haarcascades/haarcascade_frontalface_alt2.xml"
    # transform PIL image to numpy
    image_rgb = np.asarray(image)
    image_gbr = image_rgb[:, :, ::-1].copy()
    #グレースケール変換
    image_gray = cv2.cvtColor(image_gbr, cv2.COLOR_BGR2GRAY)
    #カスケード分類器の特徴量を取得する
    cascade = cv2.CascadeClassifier(cascade_path)
    #物体認識（顔認識）の実行
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
    face_image_list = []
    for rect in facerect:
        #顔だけ切り出して保存
    	x = rect[0]
    	y = rect[1]
    	width = rect[2]
    	height = rect[3]
        if width <= 180 or height <= 180:
            continue
        dst = Image.fromarray(np.uint8(image_rgb[y:y+height, x:x+width]))
        face_image_list.append(dst)
    return face_image_list

def _get_to_user_id(user_id):
    # search event_name of from_user
    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    column = 'event'
    table = 'users'
    where = 'user_id={}'.format(user_id)
    cursor, count = mysql_obj.select(column, table, where)

    if count <= 0:
        print 'register event name at first'
        return None
    event_name = cursor.next()[0]
    
    # search to_user_id whose event is the event_name
    mysql_obj = mysql_method.MysqlObject(database='photo_share_app')
    mysql_obj.connect()
    column = 'user_id'
    table = 'users'
    where = 'event=\'{}\''.format(event_name)
    cursor, count = mysql_obj.select(column, table, where)
    
    to_user_id_list = []
    for to_user_id in cursor:
        to_user_id_list.append(to_user_id[0])

    return to_user_id_list

def _generate_classifier(to_user_id_list, train_images_dir):
    # get each user's train image paths
    index_and_path_list = []
    for (i_user, to_user_id) in enumerate(to_user_id_list):
        for image_path in os.listdir(train_images_dir + '/' + str(to_user_id)):
            info = '{},{}'.format(i_user, train_images_dir + '/' + str(to_user_id) + '/' + image_path)
            index_and_path_list.append(info)
    random.shuffle(index_and_path_list)

    image_list = []
    label_list = []
    for info in index_and_path_list:
        sign = info.split(',')[0]
        path = info.split(',')[1]
        image = _import_image(path)
        image = _resize_image(image, SIZE)
        image = _format_image(image)
        label_list.append(sign)
        image_list.append(image)
    image_list = np.asarray(image_list)
    feature_list = features_generator(image_list, SIZE[0], MODEL_PATH) 
    # train classifier
    classifier = svm.SVC()
    classifier.fit(feature_list, label_list)

    return classifier

def _import_image(path):
    image = Image.open(path)
    return image

def _resize_image(image, size):
    resized_image = image.resize(size)
    return resized_image

def _format_image(image):
    image = np.asarray(image)
    image = image.flatten().astype(np.float32) / 255.0
    return image
    
def _classify_face(classifier, face_image_list):
    image_list = []
    for image in face_image_list:
        image = _resize_image(image, SIZE)
        image = _format_image(image)
        image_list.append(image)
    image_list = np.asarray(image_list)

    feature_list = features_generator(image_list, SIZE[0], MODEL_PATH)
    y_pred = classifier.predict(feature_list)
    return y_pred

