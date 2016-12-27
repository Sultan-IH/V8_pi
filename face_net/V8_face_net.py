import tensorflow as tf
import face_net._processing as pr


EPOCHS = 1000
BATCH_SIZE = 20

#TODO FIND OUT THE DIMENTIONS OF AN IMAGE

imgdir = './face_datasets/'
train_dir = "Train_data/"
test_dir = "Test_Data/"


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')


raw_lables = pr._load(img_dir=imgdir, sub_dir=train_dir, file="lables")
raw_imgs = pr._load(img_dir=imgdir, sub_dir=train_dir, file="imgs")

lables, imgs = pr._shuffle(raw_lables, raw_imgs)

sess = tf.InteractiveSession()
x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 10])

h1_Weights = weight_variable([1, 2, 3, 4]) # TODO: figure out a shape for the weights and the biases
h1_Biases = bias_variable([1, 2, 3, 4])

h1_conv = conv2d(x, h1_Weights)
h1_pooling = max_pool_2x2(h1_conv)

h2_Weights = weight_variable([1, 2, 3, 4])
h2_Biases = bias_variable([1, 2, 3, 4])

h2_conv = conv2d(x, h2_Weights)
h2_pooling = max_pool_2x2(h2_conv)

h3_Weights = weight_variable([1, 2, 3, 4])
h3_Biases = bias_variable([1, 2, 3, 4])

h3_fc = tf.nn.relu(tf.matmul(h2_pooling, h3_Weights) + h3_Biases)
keep_prob = tf.placeholder(tf.float32)

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(h3_fc, y_))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(h3_fc, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.global_variables_initializer())

for i in range(EPOCHS):
    batches = []  # TODO: figure out how to feed the dataset in batches
    list(range(0, EPOCHS, BATCH_SIZE))
    if i % 100 == 0:
        train_accuracy = accuracy.eval(feed_dict={
            x: imgs[:], y_: lables[:], keep_prob: 1.0})
        print("step %d, training accuracy %g" % (i, train_accuracy))

    train_step.run(feed_dict={x: imgs[:], y_: lables[:], keep_prob: 0.5})
