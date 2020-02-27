# fennlp v1

An out-of-the-box NLP toolkit can easily help you solve tasks such as
entity recognition, relationship extraction, text classfication and so on.
Currently it contain the following models (see "tests" dictionary for more details):
* BERT (tf2.0 layer, Chinese and English Version)
* BERT-NER (Chinese Version, 中文糖尿病标注数据集)
* BERT-CRF-NER (Chinese Version, 中文糖尿病标注数据集)
* GCN (2 layer)


# Requirement
tensorflow>=2.0

# Usage
1. clone source
```
git clone https://github.com/kyzhouhzau/fennlp.git
```
2. install package
```
python setup.py install
```
3.run model
```
python bert_ner_train.py
```

# For NER：

## input
* put train, valid and test file in "InputNER" dictionary.
* data format: reference data in  "tests\NER\InputNER\train"

e.g. "拮 抗 RANKL 对 破 骨 细 胞 的 作 用 。	O O O O B-Anatomy I-Anatomy I-Anatomy E-Anatomy O O O O"

for each line in train contains two parts, the first part "拮 抗 RANKL 对 破 骨 细 胞 的 作 用 。" is a sentence.
the second part "O O O O B-Anatomy I-Anatomy I-Anatomy E-Anatomy O O O O" is the tag for each word in the sentence.
both of them use '\t' to concatenate.

Use BERT as an tensorflow2.0's layer, See tests for more detail。

### without crf

```python
from fennlp.models import bert
bert = bert.BERT(param)
bert = bert(inputs, is_training)
```

```
python bert_ner_train.py
```

### with crf
```python
bert = self.bert([input_ids, token_type_ids, input_mask], is_training)
sequence_output = bert.get_sequence_output()  # batch,sequence,768
predict = self.dense(sequence_output)
predict = tf.reshape(predict, [self.batch_size, self.maxlen, -1])
# crf
log_likelihood, transition = self.crf(predict, Y, sequence_lengths=tf.reduce_sum(input_mask, 1))
loss = tf.math.reduce_mean(-log_likelihood)
predict, viterbi_score = self.crf.crf_decode(predict, transition, sequence_length=tf.reduce_sum(input_mask, 1))
```

```
python bert_ner_crf_train.py
```

# For GCN：

## input
data format: see files in "tests/GCN/data/README.md" for more detail.


```python
from fennlp.models import GCN
model = GCN.GCN2Layer(_HIDDEN_DIM, _NUM_CLASS, _DROP_OUT_RATE)
```

```
python train_gcn.py
```

# Status

2020/2/26: add GCN example on cora data

2020/2/25: add test example "bert_ner_train.py" and "bert_ner_test.py"






