 # Copyright 2016 TensorLayer. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Example of Synced sequence input and output.
Generate text using LSTM.

"""

import tensorflow as tf
import tensorlayer as tl
import numpy as np
import time
import re

def customized_clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data
    """
    string = re.sub(r"\n", " ", string)         # '\n'      --> ' '
    string = re.sub(r"\'s", " 's", string)      # it's      --> it 's
    string = re.sub(r"\’s", " 's", string)
    string = re.sub(r"\'ve", " have", string)   # they've   --> they have
    string = re.sub(r"\’ve", " have", string)
    string = re.sub(r"n\'t", " not", string)    # can't     --> can not
    string = re.sub(r"n\’t", " not", string)
    string = re.sub(r"\'re", " are", string)    # they're   --> they are
    string = re.sub(r"\’re", " are", string)
    string = re.sub(r"\'d", "", string)         # I'd (I had, I would) --> I
    string = re.sub(r"\’d", "", string)
    string = re.sub(r"\'ll", " will", string)   # I'll      --> I will
    string = re.sub(r"\’ll", " will", string)
    string = re.sub(r"\'", "  ", string)        # they'     --> they '
    string = re.sub(r"\’", "  ", string)        # they’     --> they ’
    string = re.sub(r"\.", " . ", string)       # they.     --> they .
    string = re.sub(r"\,", " , ", string)        # they,     --> they ,
    string = re.sub(r"\!", " ! ", string)
    string = re.sub(r"\-", "  ", string)        # "low-cost"--> lost cost
    string = re.sub(r"\(", "  ", string)       # (they)    --> ( they)
    string = re.sub(r"\)", "  ", string)       # ( they)   --> ( they )
    string = re.sub(r"\]", "  ", string)       # they]     --> they ]
    string = re.sub(r"\[", "  ", string)       # they[     --> they [
    string = re.sub(r"\?", "  ", string)       # they?     --> they ?
    string = re.sub(r"\>", "  ", string)       # they>     --> they >
    string = re.sub(r"\<", "  ", string)       # they<     --> they <
    string = re.sub(r"\=", "  ", string)        # easier=   --> easier =
    string = re.sub(r"\;", "  ", string)        # easier;   --> easier ;
    string = re.sub(r"\;", "  ", string)
    string = re.sub(r"\:", "  ", string)        # easier:   --> easier :
    string = re.sub(r"\"", "  ", string)      # easier"   --> easier "
    string = re.sub(r"\$", "  ", string)       # $380      --> $ 380
    string = re.sub(r"\_", "  ", string)        # _100     --> _ 100
    string = re.sub(r"\s{2,}", " ", string)     # Akara is    handsome --> Akara is handsome
    return string.strip().lower()               # lowercase

def customized_clean_str_(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data
    """
    string = re.sub(r"\n", " ", string)         # '\n'      --> ' '
    string = re.sub(r"\'s", " 's", string)      # it's      --> it 's
    string = re.sub(r"\’s", " 's", string)
    string = re.sub(r"\'ve", " have", string)   # they've   --> they have
    string = re.sub(r"\’ve", " have", string)
    string = re.sub(r"n\'t", " not", string)    # can't     --> can not
    string = re.sub(r"n\’t", " not", string)
    string = re.sub(r"\'re", " are", string)    # they're   --> they are
    string = re.sub(r"\’re", " are", string)
    string = re.sub(r"\'d", "", string)         # I'd (I had, I would) --> I
    string = re.sub(r"\’d", "", string)
    string = re.sub(r"\'ll", " will", string)   # I'll      --> I will
    string = re.sub(r"\’ll", " will", string)
    string = re.sub(r"\'", " ' ", string)        # they'     --> they '
    string = re.sub(r"\’", " ' ", string)        # they’     --> they '
    string = re.sub(r"\.", " . ", string)       # they.     --> they .
    string = re.sub(r"\,", " , ", string)       # they,     --> they ,
    string = re.sub(r"\-", " ", string)         # "low-cost"--> lost cost
    string = re.sub(r"\(", " ( ", string)       # (they)    --> ( they)
    string = re.sub(r"\)", " ) ", string)       # ( they)   --> ( they )
    string = re.sub(r"\!", " ! ", string)       # they!     --> they !
    string = re.sub(r"\]", " ] ", string)       # they]     --> they ]
    string = re.sub(r"\[", " [ ", string)       # they[     --> they [
    string = re.sub(r"\?", " ? ", string)       # they?     --> they ?
    string = re.sub(r"\>", " > ", string)       # they>     --> they >
    string = re.sub(r"\<", " < ", string)       # they<     --> they <
    string = re.sub(r"\=", " = ", string)        # easier=   --> easier =
    string = re.sub(r"\;", " ; ", string)        # easier;   --> easier ;
    string = re.sub(r"\;", " ; ", string)
    string = re.sub(r"\:", " : ", string)        # easier:   --> easier :
    string = re.sub(r"\"", " \" ", string)      # easier"   --> easier "
    string = re.sub(r"\$", " $ ", string)       # $380      --> $ 380
    string = re.sub(r"\_", " _ ", string)        # _100     --> _ 100
    string = re.sub(r"\s{2,}", " ", string)     # Akara is    handsome --> Akara is handsome
    return string.strip().lower()               # lowercase

def customized_read_words(input_fpath):#, dictionary):
    with open(input_fpath, "r") as f:
        words = f.read()
    # Clean the data
    words = customized_clean_str(words)
    # Split each word
    return words.split()

def customized_word2ids(words, dictionary, unk_key = 'UNK'):
    # Convert from words into indices of the specified dictionary
    word_ids = []
    for word in words:
        if dictionary.get(word) is not None:
            word_ids.append(dictionary[word])
        else:
            word_ids.append(dictionary[unk_key])
    return word_ids

def main_how_to_use_embedding_layer():
    """How to use Embedding layer, and how to convert IDs to vector,
    IDs to words, etc.
    """
    ## Step 1: Build the embedding matrix and load the existing embedding matrix.
    vocabulary_size = 50000
    embedding_size = 200
    model_file_name = "model_word2vec_50k_200"
    batch_size = None

    print("Load existing embedding matrix and dictionaries")
    all_var = tl.files.load_npy_to_any(name=model_file_name+'.npy')
    data = all_var['data']; count = all_var['count']
    dictionary = all_var['dictionary']
    reverse_dictionary = all_var['reverse_dictionary']

    tl.files.save_vocab(count, name='vocab_'+model_file_name+'.txt')

    del all_var, data, count

    load_params = tl.files.load_npz(name=model_file_name+'.npz')

    x = tf.placeholder(tf.int32, shape=[batch_size])
    y_ = tf.placeholder(tf.int32, shape=[batch_size, 1])

    emb_net = tl.layers.EmbeddingInputlayer(
                    inputs = x,
                    vocabulary_size = vocabulary_size,
                    embedding_size = embedding_size,
                    name ='embedding_layer')

    sess.run(tf.initialize_all_variables())

    tl.files.assign_params(sess, [load_params[0]], emb_net)

    emb_net.print_params()
    emb_net.print_layers()

    ## Step 2: Input word(s), output the word vector(s).
    word = b'hello'
    word_id = dictionary[word]
    print('word_id:', word_id)

    words = [b'i', b'am', b'hao', b'dong']
    word_ids = tl.files.words_to_word_ids(words, dictionary)
    context = tl.files.word_ids_to_words(word_ids, reverse_dictionary)
    print('word_ids:', word_ids)
    print('context:', context)

    vector = sess.run(emb_net.outputs, feed_dict={x : [word_id]})
    print('vector:', vector.shape)

    vectors = sess.run(emb_net.outputs, feed_dict={x : word_ids})
    print('vectors:', vectors.shape)

def main_lstm_generate_text():
    """Generate text by Synced sequence input and output.
    """
    # rnn model and update  (describtion: see tutorial_ptb_lstm.py)
    # init_scale = 0.05
    # learning_rate = 1.0
    # max_grad_norm = 5
    # num_steps = 35
    # hidden_size = 650
    # max_epoch = 6
    # max_max_epoch = 100
    # keep_prob = 0.5
    # lr_decay = 0.95
    # batch_size = 20
    init_scale = 0.1
    learning_rate = 1.0
    max_grad_norm = 5
    num_steps = 20
    hidden_size = 200
    max_epoch = 4
    max_max_epoch = 100
    keep_prob = 0.8
    lr_decay = 0.95
    batch_size = 20
    # word embedding
    vocab_size = 8000
    embedding_size = 200
    # text generation
    diversity_list = [0.5, 1.0, 1.7, 3.0] # BUG ! when 0.5
    print_length = 50

    resume = True  # load existing model, data and dictionaries
    model_file_name = "model_generate_text"

    # print("Load existing embedding matrix and dictionaries")
    # model_file_name = "model_word2vec_50k_200"
    # all_var = files.load_npy_to_any(name=model_file_name+'.npy')
    # data = all_var['data']; count = all_var['count']
    # dictionary = all_var['dictionary']
    # reverse_dictionary = all_var['reverse_dictionary']
    # files.save_vocab(count, name='vocab_'+model_file_name+'.txt')
    # del all_var, data, count
    # load_params = files.load_npz(name=model_file_name+'.npz')
    # pretrain_embedding_params = load_params[0]

    # data, count, dictionary, reverse_dictionary = \
    #         tl.files.build_words_dataset(words, vocabulary_size=vocab_size,
    #                                                         printable=True)
    if resume:
        print("Load existing data and dictionaries" + "!"*10)
        all_var = tl.files.load_npy_to_any(name=model_file_name+'.npy')
        data = all_var['data']; count = all_var['count']
        dictionary = all_var['dictionary']
        reverse_dictionary = all_var['reverse_dictionary']
    else:
        print("Load data and creat dictionaries ....")
        # words = customized_read_words(input_fpath="tensorlayer/data/trump_twitter.txt")
        words = tl.files.load_nietzsche_dataset()
        words = customized_clean_str(words)
        words = words.split()
        data, count, dictionary, reverse_dictionary = \
                    tl.files.build_words_dataset(words, vocab_size, True)
        data = customized_word2ids(words, dictionary, unk_key = 'UNK')
        data = np.asarray(data)
        del words

    print('Data size %d' % len(data))
    print('Most 5 common words (+UNK)', count[:5])
    print('Sample data', data[:10], [reverse_dictionary[i] for i in data[:10]])

    train_data = data

    print('len(train_data) {}'.format(len(train_data)))


    # seed = 'I think you are'
    # seed = "But to speak seriously, there are good grounds for"
    seed = "Well I think you are right but"
    seed = customized_clean_str(seed).split()
    print('seed : %s' % seed)

    sess = tf.InteractiveSession()

    # One int represents one word, the meaning of batch_size here is not the
    # same with MNIST example, it is the number of concurrent processes for
    # computational reasons.

    # Training and Validing
    input_data = tf.placeholder(tf.int32, [batch_size, num_steps])
    targets = tf.placeholder(tf.int32, [batch_size, num_steps])
    # Testing (Evaluation), for generate text
    input_data_test = tf.placeholder(tf.int32, [1, 1])
    targets_test = tf.placeholder(tf.int32, [1, 1])

    def inference(x, is_training, num_steps, reuse=None):
        """If reuse is True, the inferences use the existing parameters,
        then different inferences share the same parameters.
        """
        print("\nnum_steps : %d, is_training : %s, reuse : %s" %
                                                (num_steps, is_training, reuse))
        initializer = tf.random_uniform_initializer(init_scale, init_scale)
        with tf.variable_scope("model", reuse=reuse):
            tl.layers.set_name_reuse(reuse)
            network = tl.layers.EmbeddingInputlayer(
                        inputs = x,
                        vocabulary_size = vocab_size,
                        embedding_size = embedding_size,
                        E_init = tf.random_uniform_initializer(-init_scale, init_scale),
                        name ='embedding_layer')
            if is_training:
                network = tl.layers.DropoutLayer(network, keep=keep_prob, name='drop1')
            network = tl.layers.RNNLayer(network,
                        cell_fn=tf.nn.rnn_cell.BasicLSTMCell,
                        cell_init_args={'forget_bias': 0.0},# 'state_is_tuple': True},
                        n_hidden=hidden_size,
                        initializer=tf.random_uniform_initializer(-init_scale, init_scale),
                        n_steps=num_steps,
                        return_last=False,
                        name='basic_lstm_layer1')
            lstm1 = network
            if is_training:
                network = tl.layers.DropoutLayer(network, keep=keep_prob, name='drop2')
            network = tl.layers.RNNLayer(network,
                        cell_fn=tf.nn.rnn_cell.BasicLSTMCell,
                        cell_init_args={'forget_bias': 0.0}, # 'state_is_tuple': True},
                        n_hidden=hidden_size,
                        initializer=tf.random_uniform_initializer(-init_scale, init_scale),
                        n_steps=num_steps,
                        return_last=False,
                        return_seq_2d=True,
                        name='basic_lstm_layer2')
            lstm2 = network
            # Alternatively, if return_seq_2d=False, in the above RNN layer,
            # you can reshape the outputs as follow:
            # network = tl.layers.ReshapeLayer(network,
            #       shape=[-1, int(network.outputs._shape[-1])], name='reshape')
            if is_training:
                network = tl.layers.DropoutLayer(network, keep=keep_prob, name='drop3')
            network = tl.layers.DenseLayer(network,
                        n_units=vocab_size,
                        W_init=tf.random_uniform_initializer(-init_scale, init_scale),
                        b_init=tf.random_uniform_initializer(-init_scale, init_scale),
                        act = tl.activation.identity, name='output_layer')
        return network, lstm1, lstm2

    # Inference for Training
    network, lstm1, lstm2 = inference(input_data,
                            is_training=True, num_steps=num_steps, reuse=None)
    # Inference for Testing (Evaluation), generate text
    network_test, lstm1_test, lstm2_test = inference(input_data_test,
                            is_training=False, num_steps=1, reuse=True)
    y = network_test.outputs
    y_soft = tf.nn.softmax(y)
    # y_id = tf.argmax(tf.nn.softmax(y), 1)

    sess.run(tf.initialize_all_variables())

    def loss_fn(outputs, targets, batch_size, num_steps):
        # Returns the cost function of Cross-entropy of two sequences, implement
        # softmax internally.
        # outputs : 2D tensor [n_examples, n_outputs]
        # targets : 2D tensor [n_examples, n_outputs]
        # n_examples = batch_size * num_steps
        # so
        # cost is the averaged cost of each mini-batch (concurrent process).
        loss = tf.nn.seq2seq.sequence_loss_by_example(
            [outputs],
            [tf.reshape(targets, [-1])],
            [tf.ones([batch_size * num_steps])])
        cost = tf.reduce_sum(loss) / batch_size
        return cost

    # Cost for Training
    cost = loss_fn(network.outputs, targets, batch_size, num_steps)

    # Truncated Backpropagation for training
    with tf.variable_scope('learning_rate'):
        lr = tf.Variable(0.0, trainable=False)
    # You can get all trainable parameters as follow.
    # tvars = tf.trainable_variables()
    # Alternatively, you can specific the parameters for training as follw.
    #   tvars = network.all_params      $ all parameters
    #   tvars = network.all_params[1:]  $ parameters except embedding matrix
    tvars = network.all_params
    #
    grads, _ = tf.clip_by_global_norm(tf.gradients(cost, tvars),
                                      max_grad_norm)
    optimizer = tf.train.GradientDescentOptimizer(lr)
    train_op = optimizer.apply_gradients(zip(grads, tvars))

    sess.run(tf.initialize_all_variables())

    network.print_params()
    network.print_layers()
    tl.layers.print_all_variables()

    if resume:
        print("Load existing model" + "!"*10)
        load_params = tl.files.load_npz(name=model_file_name+'.npz')
        tl.files.assign_params(sess, load_params, network)


    print("\nStart learning a model to generate text")
    for i in range(max_max_epoch):
        # decrease the learning_rate after ``max_epoch``, by multipling lr_decay.
        new_lr_decay = lr_decay ** max(i - max_epoch, 0.0)
        sess.run(tf.assign(lr, learning_rate * new_lr_decay))

        # Training
        print("Epoch: %d/%d Learning rate: %.8f" % (i + 1, max_max_epoch, sess.run(lr)))
        epoch_size = ((len(train_data) // batch_size) - 1) // num_steps
        # print(epoch_

        start_time = time.time()
        costs = 0.0; iters = 0
        # reset all states at the begining of every epoch
        state1 = tl.layers.initialize_rnn_state(lstm1.initial_state)
        state2 = tl.layers.initialize_rnn_state(lstm2.initial_state)
        for step, (x, y) in enumerate(tl.iterate.ptb_iterator(train_data,
                                                    batch_size, num_steps)):
            feed_dict = {input_data: x, targets: y,
                        lstm1.initial_state: state1,
                        lstm2.initial_state: state2,
                        }
            # For training, enable dropout
            feed_dict.update( network.all_drop )
            _cost, state1, state2, _ = sess.run([cost,
                                            lstm1.final_state,
                                            lstm2.final_state,
                                            train_op],
                                            feed_dict=feed_dict
                                            )
            costs += _cost; iters += num_steps

            if step % (epoch_size // 10) == 1:
                print("%.3f perplexity: %.3f speed: %.0f wps" %
                    (step * 1.0 / epoch_size, np.exp(costs / iters),
                    iters * batch_size / (time.time() - start_time)))
        train_perplexity = np.exp(costs / iters)
        # print("Epoch: %d Train Perplexity: %.3f" % (i + 1, train_perplexity))
        print("Epoch: %d/%d Train Perplexity: %.3f" % (i + 1, max_max_epoch,
                                                            train_perplexity))

        for diversity in diversity_list:
            # Testing, generate some text from a given seed.
            state1 = tl.layers.initialize_rnn_state(lstm1_test.initial_state)
            state2 = tl.layers.initialize_rnn_state(lstm2_test.initial_state)
            # prepare the seed
            outs_id = tl.files.words_to_word_ids(seed, dictionary)
            # feed the seed to initialize the state for generation.
            for ids in outs_id[:-1]:
                a_id = np.asarray(ids).reshape(1,1)
                feed_dict = {input_data_test: a_id,
                            lstm1_test.initial_state: state1,
                            lstm2_test.initial_state: state2,
                            }
                _, state1, state2 = sess.run([y_soft, #y_id,
                                            lstm1_test.final_state,
                                            lstm2_test.final_state],
                                            feed_dict=feed_dict
                                            )
            # feed the last word in seed, and start to generate sentence.
            a_id = outs_id[-1]
            for _ in range(print_length):
                a_id = np.asarray(a_id).reshape(1,1)
                feed_dict = {input_data_test: a_id,
                            lstm1_test.initial_state: state1,
                            lstm2_test.initial_state: state2,
                            }
                out, state1, state2 = sess.run([y_soft, #y_id,
                                                lstm1_test.final_state,
                                                lstm2_test.final_state],
                                                feed_dict=feed_dict
                                                )
                a_id = tl.nlp.sample(out[0], diversity)

                outs_id.append(a_id)
            sentence = tl.files.word_ids_to_words(outs_id, reverse_dictionary)
            sentence = " ".join(sentence)
            print(diversity, ':', sentence)

        if i % 5 == 0:
            print("Save model, data and dictionaries" + "!"*10);
            tl.files.save_npz(network_test.all_params, name=model_file_name+'.npz')
            tl.files.save_any_to_npy(save_dict={'data': data, 'count': count,
                'dictionary': dictionary, 'reverse_dictionary':
                reverse_dictionary}, name=model_file_name+'.npy')



if __name__ == '__main__':
    sess = tf.InteractiveSession()
    # How to use a pretrained embedding matrix.
    # main_how_to_use_embedding_layer()
    # How to generate text from a given context.
    main_lstm_generate_text()














#
