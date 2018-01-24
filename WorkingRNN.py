import tensorflow as tf
import os
import format
saveDIR = "/media/sinclair/UBUNTU 16_0/TestZone/Models"
element_size = 128 #128 down
time_steps = 31 #31 across
num_classes = 3 #juno or silence or talking
batch_size = 128
hidden_layer_size = 128

_inputs = tf.placeholder(tf.float32,shape=[None,time_steps,element_size],name ="inputs")
y = tf.placeholder(tf.float32, shape=[None, num_classes], name='inputs')

rnn_cell = tf.contrib.rnn.BasicRNNCell(hidden_layer_size) #first layer of network
outputs, _ = tf.nn.dynamic_rnn(rnn_cell, _inputs, dtype=tf.float32)

Wl = tf.Variable(tf.truncated_normal([hidden_layer_size, num_classes], mean=0,stddev=.01))
bl = tf.Variable(tf.truncated_normal([num_classes],mean=0,stddev=.01))

def get_linear_layer(vector):
    return tf.matmul(vector, Wl) + bl

last_rnn_output = outputs[:,-1,:]
final_output = get_linear_layer(last_rnn_output)

softmax = tf.nn.softmax_cross_entropy_with_logits(logits=final_output,labels=y)

cross_entropy = tf.reduce_mean(softmax)
train_step = tf.train.RMSPropOptimizer(0.001, 0.9).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(final_output,1))
accuracy = (tf.reduce_mean(tf.cast(correct_prediction, tf.float32)))*100

saver = tf.train.Saver(max_to_keep=5)

sess=tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

test_batch_x, test_batch_y = format.get_batch(100)
for i in range(3001):
    #batch_x is an array of batch size x time steps x element size, all values containing a greyscale
    #batch_y is an array of batch size x num classes, with one of the num classes being 1 for the correct label.
    batch_x, batch_y = format.get_batch(batch_size)
    sess.run(train_step,feed_dict={_inputs:batch_x,y:batch_y})
    print(i)
    if i % 100 == 0:
        acc = sess.run(accuracy, feed_dict={_inputs:batch_x,y:batch_y})
        loss = sess.run(cross_entropy, feed_dict={_inputs:batch_x,y:batch_y})

        saver.save(sess, os.path.join(saveDIR, "Name_model"), global_step=i)
        print("Iter "+str(i)+", Minibatch Loss= " + \
                "{:.6f}".format(loss) + ", Training Accuracy= " + \
                "{:.5f}".format(acc))

print('Testing Accuracy:', sess.run(accuracy, feed_dict={_inputs: test_data, y: test_label}))
