'''xor in tensorflow'''

import tensorflow as tf

'''
    Construct the network
'''

# Input vector #
# Depends on user data
i = tf.placeholder(tf.float32, shape=[None, 2])
y_ = tf.placeholder(tf.float32, shape=[None, 1])

W = tf.Variable(tf.random_uniform([2, 3]))
b = tf.Variable(tf.ones([1, 3]))

hidden = tf.nn.sigmoid(tf.matmul(i, W) + b)

W2 = tf.Variable(tf.random_uniform([3, 1]))
b2 = tf.Variable(tf.ones([1, 1]))

y = tf.nn.sigmoid(tf.matmul(hidden,W2) + b2)

obj_fn = tf.reduce_mean((y_ - y)**2)

optim = tf.train.GradientDescentOptimizer(.1).minimize(obj_fn)

'''
    Train and test
'''

# Input vector test
inp_vec = [[1., 0.], [0., 1.], [1., 1.], [0., 0.]]
solutions = [[1.], [1.], [0.], [0.]]

with tf.Session() as sess:
    # Tf housekeeping
    #sess.run( tf.initialize_all_variables() )
    sess.run(tf.global_variables_initializer())

    for step in range(20000):
        a = sess.run(optim, feed_dict={i: inp_vec, y_: solutions})

    print('\nSolution')
    print(sess.run(y, feed_dict={i: inp_vec}))
