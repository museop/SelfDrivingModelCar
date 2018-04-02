import tensorflow as tf
import scipy.misc

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W, stride):
    return tf.nn.conv2d(x, W, strides=[1, stride, stride, 1], padding='VALID')

class CNN_model(object):

    def __init__(self, dropout_prob=0.2):
        x  = tf.placeholder(tf.float32, shape=[None, 66, 200, 3], name='x')
        y_ = tf.placeholder(tf.float32, shape=[None, 1])
        keep_prob = tf.placeholder(tf.float32, name='keep_prob')
        x_image = x

        # first convolutional layer
        self.W_conv1 = weight_variable([5, 5, 3, 24])
        self.b_conv1 = bias_variable([24])
        self.h_conv1 = tf.nn.relu(conv2d(x_image, self.W_conv1, 2) + self.b_conv1)

        # second convolutional layer
        self.W_conv2 = weight_variable([5, 5, 24, 36])
        self.b_conv2 = bias_variable([36])
        self.h_conv2 = tf.nn.relu(conv2d(self.h_conv1, self.W_conv2, 2) + self.b_conv2)
        
        # third convolutional layer
        self.W_conv3 = weight_variable([5, 5, 36, 48])
        self.b_conv3 = bias_variable([48])
        self.h_conv3 = tf.nn.relu(conv2d(self.h_conv2, self.W_conv3, 2) + self.b_conv3)
       
        # fourth convolutional layer
        self.W_conv4 = weight_variable([3, 3, 48, 64])
        self.b_conv4 = bias_variable([64])
        self.h_conv4 = tf.nn.relu(conv2d(self.h_conv3, self.W_conv4, 1) + self.b_conv4)
      
        # fifth convolutional layer
        self.W_conv5 = weight_variable([3, 3, 64, 64])
        self.b_conv5 = bias_variable([64])
        self.h_conv5 = tf.nn.relu(conv2d(self.h_conv4, self.W_conv5, 1) + self.b_conv5)
     
        # FCL 1
        self.W_fc1 = weight_variable([1152, 1164])
        self.b_fc1 = bias_variable([1164])
        self.h_conv5_flat = tf.reshape(self.h_conv5, [-1, 1152])
        self.h_fc1 = tf.nn.relu(tf.matmul(self.h_conv5_flat, self.W_fc1) + self.b_fc1, name='fc1')
        self.h_fc1_drop = tf.nn.dropout(self.h_fc1, keep_prob)
       
        # FCL 2
        self.W_fc2 = weight_variable([1164, 100])
        self.b_fc2 = bias_variable([100])
        self.h_fc2 = tf.nn.relu(tf.matmul(self.h_fc1_drop, self.W_fc2) + self.b_fc2, name='fc2')
        self.h_fc2_drop = tf.nn.dropout(self.h_fc2, keep_prob)

        # FCL 3
        self.W_fc3 = weight_variable([100, 50])
        self.b_fc3 = bias_variable([50])
        self.h_fc3 = tf.nn.relu(tf.matmul(self.h_fc2_drop, self.W_fc3) + self.b_fc3, name='fc3')
        self.h_fc3_drop = tf.nn.dropout(self.h_fc3, keep_prob)

        #FCL 4
        self.W_fc4 = weight_variable([50, 10])
        self.b_fc4 = bias_variable([10])
        self.h_fc4 = tf.nn.relu(tf.matmul(self.h_fc3_drop, self.W_fc4) + self.b_fc4, name='fc4')
        self.h_fc4_drop = tf.nn.dropout(self.h_fc4, keep_prob)

        # Output
        self.W_fc5 = weight_variable([10, 1])
        self.b_fc5 = bias_variable([1])
        y = tf.multiply(tf.atan(tf.matmul(self.h_fc4_drop, self.W_fc5) + self.b_fc5), 2, name='y') #scale the atan output

        self.x = x
        self.y_ = y_
        self.y = y
        self.keep_prob = keep_prob
        self.fc2 = self.h_fc2
        self.fc3 = self.h_fc3
    
    def predict(self, sess, img):
        img = scipy.misc.imresize(img[-150:], [66, 200]) / 255.0
        prediction_value = sess.run(self.y, feed_dict={self.x: [img], self.keep_prob: 1.0})[0][0]
        return prediction_value

    
