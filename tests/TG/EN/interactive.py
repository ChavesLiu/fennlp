#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:Kaiyin Zhou
"""
import tensorflow as tf
from fennlp.models import gpt2
from fennlp.tools import gpt2_init_weights_from_checkpoint
from fennlp.datas.checkpoint import LoadCheckpoint
from fennlp.tokenizers import gpt2_tokenization
from fennlp.sample import samples

# 载入参数
load_check = LoadCheckpoint(langurage='en', model="gpt2", paramaters="medium")
param, vocab_file, model_path, encoder_file = load_check.load_gpt2_param()
print(param)

tokenizer = gpt2_tokenization.FullTokenizer(encoder_file, vocab_file)


# 构建模型
class GenGPT2(tf.keras.Model):
    def __init__(self, param, **kwargs):
        super(GenGPT2, self).__init__(**kwargs)
        self.model = gpt2.GPT2(param)

    def call(self, inputs, past=None, is_training=True):
        out = self.model(inputs, past, is_training)
        return out

    def predict(self, inputs, past=None, is_training=False):
        return self(inputs, past, is_training)


model = GenGPT2(param)
model.build(input_shape=(param.batch_size, param.maxlen))
model.summary()

gpt2_init_weights_from_checkpoint(model, model_path, param.n_layer)
generated = 0
nsamples = 3
while True:
    raw_text = input("\nInput >>> ")
    while not raw_text:
        print('Input should not be empty!')
        raw_text = input("\nInput >>> ")
    context_tokens = tokenizer.tokenize(raw_text)
    generated = 0
    for _ in range(nsamples // param.batch_size):
        context = [context_tokens for _ in range(param.batch_size)]

        out = samples.sample_sequence(model, param, length=100,
                                      context=context,
                                      temperature=0.9,
                                      top_k=40, top_p=1)[:, len(context_tokens):]
        for i in range(param.batch_size):
            generated += 1
            text = tokenizer.convert_tokens_to_string(out[i].numpy())
            print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
            print(text)
    print("=" * 80)
