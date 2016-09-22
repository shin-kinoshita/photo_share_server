import tensorflow as tf
import numpy as np
import os
import shutil
import random
from PIL import Image

IMAGE_SIZE = 56
IMAGE_PIXELS = IMAGE_SIZE*IMAGE_SIZE*3
flags = tf.app.flags
FLAGS = flags.FLAGS

flags.DEFINE_string('saverPath', './tmp/face_model.ckpt', 'File name of .ckpt data')
flags.DEFINE_integer('batch_size', 100, 'Batch size'
                     'Must divide evenly into the dataset sizes.')

flags.DEFINE_string('export_dir', './tmp/face-export', 'directory of export')
flags.DEFINE_string('conv_data_dir', './data', '')
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
        files = []
        if not os.path.isdir(d):
            continue

        for filename in os.listdir(d):
            if filename.endswith(".jpg"):
                files.append(filename)
                file_num += 1
        trains = []
        tests = []
        divider = file_num*2/3
        trains = files[:divider]
        tests = files[divider:]
        for filename in trains:
            f_train.write(d + "/" + filename + " " + str(i)+"\r\n")
        for filename in tests:
            f_test.write(d + "/" + filename + " " + str(i)+"\r\n")
        i += 1

    if path2 != None:
        directoryList = os.listdir(path2)
        i = 0
        for directory in directoryList:
            d = path2 + "/" + directory
            file_num = 0
            i += 1
            if os.path.isdir(d):
                files = []
                tests = []
                for filename in os.listdir(d):
                    if filename.endswith(".jpg"):
                        files.append(filename)
                        file_num += 1
                for filename in files:
                    f_test.write(d + "/" + filename + " " + str(i)+"\r\n")
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

def trans_sign_to_label(sign_list, num_classes):
    label_list = np.zeros([len(sign_list), num_classes])
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

def main():
    NUM_CLASSES = makeDocument(FLAGS.conv_data_dir)
    g = tf.Graph()
    with g.as_default():
        x = tf.placeholder("float", shape=[None, IMAGE_PIXELS])
        y_ = tf.placeholder("float", shape=[None, NUM_CLASSES])

        W_conv1 = weight_variable([3, 3, 3, 32],"W_conv1")
        b_conv1 = bias_variable([32],"b_conv1")
        x_image = tf.reshape(x, [-1, IMAGE_SIZE, IMAGE_SIZE, 3])
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

        W_fc1 = weight_variable([IMAGE_SIZE * IMAGE_SIZE * 128 / 64, 1024],"W_fc1")
        b_fc1 = bias_variable([1024],"b_fc1")
        h_pool3_flat = tf.reshape(h_pool3, [-1, IMAGE_SIZE * IMAGE_SIZE * 128 / 64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool3_flat, W_fc1) + b_fc1)

        keep_prob = tf.placeholder("float")
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

        train_file_list, train_sign_list = get_file_info(FLAGS.trainText)
        print len(train_file_list)
        print len(train_sign_list)
        test_file_list, test_sign_list = get_file_info(FLAGS.testText)
        print len(test_file_list)
        print len(test_sign_list)
        
        saver = tf.train.Saver()
        sess = tf.Session()

        W_fc2 = weight_variable([1024, NUM_CLASSES])
        b_fc2 = bias_variable([NUM_CLASSES])
        y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
        cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
        train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
        correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        sess.run(tf.initialize_all_variables())

        for step in range(100):
            train_acc = 0
            loop_count = len(train_file_list) /FLAGS.batch_size + 1

            train_file_gen = list_generator(train_file_list, FLAGS.batch_size)
            train_sign_gen = list_generator(train_sign_list, FLAGS.batch_size)
            test_file_gen = list_generator(test_file_list, FLAGS.batch_size)
            test_sign_gen = list_generator(test_sign_list, FLAGS.batch_size)
        
            train_image_list = np.zeros([1, IMAGE_PIXELS])
            train_label_list = np.zeros([1, NUM_CLASSES])
            test_image_list = np.zeros([1, IMAGE_PIXELS])
            test_label_list = np.zeros([1, NUM_CLASSES])
            
            test_image_list  = import_image_list(test_file_list)
            test_label_list  = trans_sign_to_label(test_sign_list, NUM_CLASSES)
            image_list = import_image_list(test_file_list)
            label_list = trans_sign_to_label(test_sign_list, NUM_CLASSES)

            for i in range(loop_count):
                train_file_list = train_file_gen.next()
                train_sign_list = train_sign_gen.next()
                
                train_image_list  = import_image_list(train_file_list)
                train_label_list  = trans_sign_to_label(train_sign_list, NUM_CLASSES)
                
                train_step.run({x: train_image_list, y_: train_label_list, keep_prob: 0.5}, sess)
                train_acc += accuracy.eval({x: test_image_list, y_: test_label_list, keep_prob: 1.0}, sess)
            print ("step {0}, training accuracy {1}".format(step, train_acc / loop_count))
        #CNN accuracyCheck
        image_list = import_image_list(test_file_list)
        label_list = trans_sign_to_label(test_sign_list, NUM_CLASSES)
        test_acc = accuracy.eval({x: image_list, y_: label_list, keep_prob: 1.0}, sess)
        print "test accuracy {0}".format(test_acc)
        save_path = saver.save(sess, FLAGS.saverPath)
        print("Model saved in file: %s" % save_path)

if __name__ == '__main__':
    main()
