import tensorflow as tf
import numpy as np
import os
import shutil
import random
from sklearn import svm
from sklearn.metrics import accuracy_score
from PIL import Image

IMAGE_SIZE = 56
IMAGE_PIXELS = IMAGE_SIZE*IMAGE_SIZE*3
flags = tf.app.flags
FLAGS = flags.FLAGS

flags.DEFINE_string('saverPath', './tmp/face_model.ckpt', 'File name of .ckpt data')
flags.DEFINE_integer('batch_size', 100, 'Batch size'
                     'Must divide evenly into the dataset sizes.')

flags.DEFINE_string('export_dir', './tmp/face-export', 'directory of export')
flags.DEFINE_string('transfer_data_dir', './data', '')
flags.DEFINE_string('portrait_data_dir', './data', '')
flags.DEFINE_string('tmp_dir', './tmp', '')
flags.DEFINE_string('trainText', './tmp/train.txt', '')
flags.DEFINE_string('testText', './tmp/test.txt', '')

def makeDocument(path,path2=None):
    f_train = open(FLAGS.trainText, 'w')
    f_test = open(FLAGS.testText, 'w')
    directoryList = os.listdir(path)
    i = 0
    for directory in directoryList:
        d = path + "/" + directory
        file_num = 0
        if not os.path.isdir(d):
            continue

        files = []
        for filename in os.listdir(d):
            if filename.endswith(".jpg"):
                files.append(filename)
                file_num += 1
        for filename in files:
            f_train.write(d + "/" + filename + " " + str(i)+"\r\n")
        i += 1

    if path2 != None:
        directoryList = os.listdir(path2)
        i = 0
        for directory in directoryList:
            d = path2 + "/" + directory
            file_num = 0
            if not os.path.isdir(d):
                continue
            files = []
            tests = []
            for filename in os.listdir(d):
                if filename.endswith(".jpg"):
                    files.append(filename)
                    file_num += 1
            for filename in files:
                f_test.write(d + "/" + filename + " " + str(i)+"\r\n")
            i += 1
    else:
        pass
    f_train.close()
    f_test.close()
    return i

def shuffle_data(features, labels):
    new_features, new_labels = [], []
    index_shuf = range(len(features))
    random.shuffle(index_shuf)
    for i in index_shuf:
        new_features.append(features[i])
        new_labels.append(labels[i])
    return new_features, new_labels

def get_file_info(doc_path):
    f = open(doc_path, 'r')
    file_list = []
    label_list = []
    for line in f:
        line = line.rstrip()
        l = line.split()
        file_name = l[0]
        label = l[1]
        file_list.append(file_name)
        label_list.append(label)
    return shuffle_data(file_list, label_list)
    
def list_generator(list, batch_size):
    count = len(list)
    for i in range(0, count, batch_size):
        yield list[i:i+batch_size]

def import_image_list(file_list):
    size = IMAGE_SIZE, IMAGE_SIZE
    image_list = []
    for path in file_list:
        image = Image.open(path)
        image = image.resize(size)
        #image.thumbnail(size, Image.ANTIALIAS)
        image = np.asarray(image)
        image_list.append(image.flatten().astype(np.float32) / 255.0)
    return np.asarray(image_list)

def trans_sign_to_label(sign_list):
    label_list = np.zeros([len(sign_list), NUM_CLASSES])
    for (i, sign) in enumerate(sign_list):
        label_list[i][int(sign)] = 1

    return np.asarray(label_list)

def make_SVM_label_list(sign_list):
    label_list = []
    for (i, sign) in enumerate(sign_list):
        label_list.append(int(sign))
    
    return np.asarray(label_list)

if os.path.exists(FLAGS.export_dir):
    shutil.rmtree(FLAGS.export_dir)

def weight_variable(shape, Name=None):
    if Name == None:
        initial = tf.truncated_normal(shape, stddev=0.1)
    else:
        initial = tf.truncated_normal(shape, stddev=0.1, name=Name)
    return tf.Variable(initial)

def bias_variable(shape, Name=None):
    if Name == None:
        initial = tf.constant(0.1, shape=shape)
    else:
        initial = tf.constant(0.1, shape=shape,name=Name)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')

def features_generator(image_list, image_size, model_path):
    image_pixels = image_size * image_size * 3
    g = tf.Graph()
    with g.as_default():
        x = tf.placeholder("float", shape=[None, image_pixels])
        #y_ = tf.placeholder("float", shape=[None, NUM_CLASSES])

        W_conv1 = weight_variable([3, 3, 3, 32],"W_conv1")
        b_conv1 = bias_variable([32],"b_conv1")
        x_image = tf.reshape(x, [-1, image_size, image_size, 3])
        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
        h_pool1 = max_pool_2x2(h_conv1)

        W_conv2 = weight_variable([3, 3, 32, 64],"W_conv2")
        b_conv2 = bias_variable([64],"b_conv2")
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
        h_pool2 = max_pool_2x2(h_conv2)

        W_conv3 = weight_variable([3, 3, 64, 128],"W_conv3")
        b_conv3 = bias_variable([128],"b_conv3")
        h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3) + b_conv3)
        h_pool3 = max_pool_2x2(h_conv3)

        W_fc1 = weight_variable([image_size * image_size * 128 / 64, 1024],"W_fc1")
        b_fc1 = bias_variable([1024],"b_fc1")
        h_pool3_flat = tf.reshape(h_pool3, [-1, image_size * image_size * 128 / 64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool3_flat, W_fc1) + b_fc1)

        keep_prob = tf.placeholder("float")
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

        saver = tf.train.Saver()
        sess = tf.Session()
        saver.restore(sess, model_path)

        features = sess.run(h_fc1, {x: image_list})

    return features

def main():
    NUM_CLASSES = makeDocument(FLAGS.transfer_data_dir,FLAGS.portrait_data_dir)
    train_file_list, train_sign_list = get_file_info(FLAGS.trainText)
    print 'length of train_file_list: {} '.format(len(train_file_list))
    print 'length of train_sign_list: {}'.format(len(train_sign_list))
    test_file_list, test_sign_list = get_file_info(FLAGS.testText)
    print 'length of test_file_list: {}'.format(len(test_file_list))
    print 'length of test_sign_list: {}'.format(len(test_sign_list))

    print("Model restored.")

    #make test-data
    print("Making test-data...")
    test_image_list = np.zeros([1, IMAGE_PIXELS])
    test_label_list = np.zeros([1, NUM_CLASSES])
    test_image_list = import_image_list(test_file_list)
    test_label_list = make_SVM_label_list(test_sign_list)
    features = features_generator(test_image_list, IMAGE_SIZE, FLAGS.saverPath)
    test_feature_list = []
    for j in range(len(test_image_list)):
        test_feature_list.append(features[j])
    print("Got test-data!!")

    #SVM
    print("Making training-data")
    train_image_list = np.zeros([1, IMAGE_PIXELS])
    train_label_list = np.zeros([1, NUM_CLASSES])
    train_image_list  = import_image_list(train_file_list)
    train_label_list  = make_SVM_label_list(train_sign_list)
    features = features_generator(train_image_list, IMAGE_SIZE, FLAGS.saverPath)
    train_feature_list = []
    for j in range(len(train_image_list)):
        train_feature_list.append(features[j])
    
    print("SVM Learning")
    clf = svm.SVC()
    clf.fit(train_feature_list, train_label_list)

    y_pred = clf.predict(test_feature_list)
    print "Accuracy: %.3f" % accuracy_score(test_label_list, y_pred)

if __name__ == '__main__':
    main()
