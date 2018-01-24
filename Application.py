import tensorflow as tf
import os
import format
class RNN:
    def __init__(self):
        print("starting RNN")
        saveDIR = "/media/sinclair/SINCLAIR32/TestZone/Models"
        element_size = 128 #128 down
        time_steps = 31 #31 across
        num_classes = 3 #juno or silence or talking
        batch_size = 128
        hidden_layer_size = 128

        tf.reset_default_graph()
        self._inputs = tf.placeholder(tf.float32,shape=[None,time_steps,element_size],name ="inputs")
        y = tf.placeholder(tf.float32, shape=[None, num_classes], name='inputs')

        rnn_cell = tf.contrib.rnn.BasicRNNCell(hidden_layer_size) #first layer of network
        outputs, _ = tf.nn.dynamic_rnn(rnn_cell, self._inputs, dtype=tf.float32)

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
        self.prediction=tf.argmax(final_output,1)
        self.values = final_output
        saver = tf.train.Saver()

        sess=tf.InteractiveSession()
        sess.run(tf.global_variables_initializer())

        saver.restore(sess, os.path.join("Models/","Name_model-800"))
        print("ending RNN")
    def get_pred(self,index):
        test_x=format.test(index)
        return self.prediction.eval(feed_dict={self._inputs:test_x})
    