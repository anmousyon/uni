import tensorflow as tf
import numpy as np

'''
    Construct the network
'''

# Input vector #
# Depends on user data
i = tf.placeholder(tf.float32, shape=[3,1]) # (3x1)

W = tf.Variable( tf.random_uniform([2,3]) )
b = tf.Variable( tf.ones([2,1]) )

# Output
y = tf.nn.sigmoid( tf.matmul(W,i) + b)

'''
    Test the setup
'''

# Input vector test
inp_vec = np.array([.2,.3,.4]) # (3,)
inp_vec.shape = (3,1)

with tf.Session() as sess:
    # Tf housekeeping
    sess.run( tf.initialize_all_variables() )

    print('\nRandom weight matrix')
    print(sess.run (W))

    print ('\nSolution')
    print (sess.run(y, feed_dict={i:inp_vec}))
