# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
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
import numpy as np


def convert_example(example, tokenizer, is_test=False, language='en'):
    """
    Builds model inputs from a sequence for sequence classification tasks. 
    It use `jieba.cut` to tokenize text.

    Args:
        example(obj:`list[str]`): List of input data, containing text and label if it have label.
        tokenizer(obj: paddlenlp.data.JiebaTokenizer): It use jieba to cut the chinese string.
        is_test(obj:`False`, defaults to `False`): Whether the example contains label or not.

    Returns:
        query_ids(obj:`list[int]`): The list of query ids.
        title_ids(obj:`list[int]`): The list of title ids.
        query_seq_len(obj:`int`): The input sequence query length.
        title_seq_len(obj:`int`): The input sequence title length.
        label(obj:`numpy.array`, data type of int64, optional): The input label if not is_test.
    """
    if language == 'ch':
        q_name = "query"
        t_name = "title"
        label = "label"
    else:
        q_name = "sentence1"
        t_name = "sentence2"
        label = "labels"

    query, title = example[q_name], example[t_name]
    query_ids = np.array(tokenizer.encode(query), dtype="int64")
    query_seq_len = np.array(len(query_ids), dtype="int64")
    title_ids = np.array(tokenizer.encode(title), dtype="int64")
    title_seq_len = np.array(len(title_ids), dtype="int64")
    result = [query_ids, title_ids, query_seq_len, title_seq_len]
    if not is_test:
        label = np.array(example[label], dtype="int64")
        result.append(label)
    return result


def preprocess_prediction_data(data, tokenizer):
    """
    It process the prediction data as the format used as training.

    Args:
        data (obj:`List[List[str, str]]`): 
            The prediction data whose each element is a text pair. 
            Each text will be tokenized by jieba.lcut() function.
        tokenizer(obj: paddlenlp.data.JiebaTokenizer): It use jieba to cut the chinese string.

    Returns:
        examples (obj:`list`): The processed data whose each element 
            is a `list` object, which contains 

            - query_ids(obj:`list[int]`): The list of query ids.
            - title_ids(obj:`list[int]`): The list of title ids.
            - query_seq_len(obj:`int`): The input sequence query length.
            - title_seq_len(obj:`int`): The input sequence title length.

    """
    examples = []
    for query, title in data:
        query_ids = tokenizer.encode(query)
        title_ids = tokenizer.encode(title)
        examples.append([query_ids, title_ids, len(query_ids), len(title_ids)])
    return examples


def preprocess_data(data, tokenizer, language):
    """
    It process the prediction data as the format used as training.

    Args:
        data (obj:`List[List[str, str]]`): 
            The prediction data whose each element is a text pair. 
            Each text will be tokenized by jieba.lcut() function.
        tokenizer(obj: paddlenlp.data.JiebaTokenizer): It use jieba to cut the chinese string.

    Returns:
        examples (obj:`list`): The processed data whose each element 
            is a `list` object, which contains 

            - query_ids(obj:`list[int]`): The list of query ids.
            - title_ids(obj:`list[int]`): The list of title ids.
            - query_seq_len(obj:`int`): The input sequence query length.
            - title_seq_len(obj:`int`): The input sequence title length.

    """
    if language == 'ch':
        q_name = "query"
        t_name = "title"
    else:
        q_name = "sentence1"
        t_name = "sentence2"
    examples = []
    for example in data:
        query_ids = tokenizer.encode(example[q_name])
        title_ids = tokenizer.encode(example[t_name])
        examples.append([query_ids, title_ids, len(query_ids), len(title_ids)])
    return examples


def get_idx_from_word(word, word_to_idx, unk_word):
    if word in word_to_idx:
        return word_to_idx[word]
    return word_to_idx[unk_word]


class CharTokenizer:
    def __init__(self, vocab, language):
        self.tokenizer = list
        self.vocab = vocab
        self.language = language

    def encode(self, sentence):
        if self.language == 'ch':
            words = self.tokenizer(sentence)
        else:
            words = sentence.strip().split()
        return [
            get_idx_from_word(word, self.vocab.token_to_idx,
                              self.vocab.unk_token) for word in words
        ]

    def tokenize(self, sentence, wo_unk=True):
        return sentence.strip().split()

    def convert_tokens_to_string(self, tokens):
        return ' '.join(tokens)

    def convert_tokens_to_ids(self, tokens):
        # tocheck
        pass
