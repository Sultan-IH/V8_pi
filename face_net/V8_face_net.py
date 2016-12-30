import tensorflow as tf
import face_net._processing as pr
from face_net._processing import WIDTH, HEIGHT, NUM_PEOPLE  # Standartsized sizes for the images

SIZE_OF_TRAIN_SET = 219  # Approx
EPOCHS = 30
BATCH_SIZE = 20
"""
What I need to do:
Move the function from _capture to _processing
Use the same function to isolate the face from an image.

"""

imgdir = './face_datasets/'
train_dir = "Train_data/"
test_dir = "Test_Data/"

# Load the datasets
raw_labels = pr._load(img_dir=imgdir, sub_dir=train_dir, file="labels")
raw_imgs = pr._load(img_dir=imgdir, sub_dir=train_dir, file="imgs")

test_images = [raw_imgs[11], raw_imgs[25], raw_imgs[44], raw_imgs[199]]  # armaan, jessica, micah and tal

# Split them into chunks
img_batches = list(pr.chunky(raw_imgs, BATCH_SIZE))
lables_batches = list(pr.chunky(raw_labels, BATCH_SIZE))

test_batch_img = img_batches[4]
test_batch_labels = lables_batches[4]

# Shuffle the chunks
lables, imgs = pr.sim_shuffle(lables_batches, img_batches)

assert len(lables) == len(imgs)

"""   Setting up the computation graph   """

print("Setting up the graph")


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


sess = tf.InteractiveSession()
x = tf.placeholder(tf.float32, shape=[None, HEIGHT, WIDTH])
y_ = tf.placeholder(tf.float32, shape=[None, NUM_PEOPLE])

h1_Weights = weight_variable([5, 5, 1, 15])  # TODO: figure out a shape for the weights and the biases
h1_Biases = bias_variable([15])

x_image = tf.reshape(x, [-1, WIDTH, HEIGHT, 1])
h1_conv = tf.nn.relu(conv2d(x_image, h1_Weights) + h1_Biases)
h1_pooling = max_pool_2x2(h1_conv)

h2_Weights = weight_variable([5, 5, 15, 30])
h2_Biases = bias_variable([30])

h2_conv = tf.nn.relu(conv2d(h1_pooling, h2_Weights) + h2_Biases)
h2_pooling = max_pool_2x2(h2_conv)
h2_pool_flat = tf.reshape(h2_pooling, [-1, 100 * 113 * 30])

# Densely connected layer with 1024 neurons
h3_Weights = weight_variable([100 * 113 * 30, 1024])
h3_Biases = bias_variable([1024])

h3_fc = tf.nn.relu(tf.matmul(h2_pool_flat, h3_Weights) + h3_Biases)

h4_Weights = weight_variable([1024, 4])
h4_Biases = bias_variable([4])

Y_ = tf.matmul(h3_fc, h4_Weights) + h4_Biases

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(Y_, y_))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(Y_, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

sess.run(tf.initialize_all_variables())
print("Finished setting up the graph. ")

print("Starting training...")

for i in range(EPOCHS):
    lables, imgs = pr.sim_shuffle(lables, imgs)

    for b in range(len(imgs)):
        train_step.run(feed_dict={x: imgs[b], y_: lables[b]})
        print("Batch number : {0}".format(b))

    train_accuracy = accuracy.eval(feed_dict={x: test_batch_img, y_: test_batch_labels})
    print("Completed epoch: {0}, accuracy: {1}".format(i, train_accuracy))

    print("Computed probabilities: \n {0}".format(sess.run(Y_, feed_dict={x: test_images})))
