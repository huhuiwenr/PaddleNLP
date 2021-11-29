# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
# Copyright 2018 Google AI, Google Brain and the HuggingFace Inc. team.
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
import os
import io
import importlib
import json
from collections import OrderedDict
from paddlenlp.transformers import *
from paddlenlp.utils.downloader import COMMUNITY_MODEL_PREFIX, get_path_from_url
from paddlenlp.utils.env import MODEL_HOME
from paddlenlp.utils.log import logger

__all__ = ["AutoTokenizer", ]

TOKENIZER_MAPPING_NAMES = OrderedDict([
    # Base model mapping
    ("AlbertTokenizer", "albert"),
    ("BartTokenizer", "bart"),
    ("BigBirdTokenizer", "bigbird"),
    ("ConvBertTokenizer", "convbert"),
    ("DistilBertTokenizer", "distilbert"),
    ("ElectraTokenizer", "electra"),
    ("SkepTokenizer", "skep"),
    ("ErnieCtmTokenizer", "ernie-ctm"),
    ("ErnieDocTokenizer", "ernie-doc"),
    ("ErnieGramTokenizer", "ernie-gram"),
    ("ErnieTokenizer", "ernie"),
    ("GPTTokenizer", "gpt"),
    ("MPNetTokenizer", "mpnet"),
    ("NeZhaTokenizer", "nezha"),
    ("RobertaTokenizer", "roberta"),
    ("RoFormerTokenizer", "roformer"),
    ("TinyBertTokenizer", "tinybert"),
    ("BertTokenizer", "bert"),
    ("UnifiedTransformerTokenizer", "unified_transformer"),
    ("UNIMOTokenizer", "unimo"),
    ("XLNetTokenizer", "xlnet"),
])


def get_configurations():
    albert = tuple(AlbertPretrainedModel.pretrained_init_configuration.keys())
    bart = tuple(BartPretrainedModel.pretrained_init_configuration.keys())
    bigbird = tuple(BigBirdPretrainedModel.pretrained_init_configuration.keys())
    convbert = tuple(ConvBertPretrainedModel.pretrained_init_configuration.keys(
    ))
    distilbert = tuple(
        DistilBertPretrainedModel.pretrained_init_configuration.keys())
    electra = tuple(ElectraPretrainedModel.pretrained_init_configuration.keys())
    skep = tuple(SkepPretrainedModel.pretrained_init_configuration.keys())
    erniectm = tuple(ErnieCtmPretrainedModel.pretrained_init_configuration.keys(
    ))
    erniedoc = tuple(ErnieDocPretrainedModel.pretrained_init_configuration.keys(
    ))
    erniegram = tuple(ErnieGramModel.pretrained_init_configuration.keys())
    ernie = tuple(ErniePretrainedModel.pretrained_init_configuration.keys())
    gpt = tuple(GPTPretrainedModel.pretrained_init_configuration.keys())
    mpnet = tuple(MPNetPretrainedModel.pretrained_init_configuration.keys())
    nezha = tuple(NeZhaPretrainedModel.pretrained_init_configuration.keys())
    roberta = tuple(RobertaPretrainedModel.pretrained_init_configuration.keys())
    roformer = tuple(RoFormerPretrainedModel.pretrained_init_configuration.keys(
    ))
    tinybert = tuple(TinyBertPretrainedModel.pretrained_init_configuration.keys(
    ))
    bert = tuple(BertPretrainedModel.pretrained_init_configuration.keys())
    unifiedtransformer = tuple(
        UnifiedTransformerModel.pretrained_init_configuration.keys())
    unimo = tuple(UNIMOPretrainedModel.pretrained_init_configuration.keys())
    xlnet = tuple(XLNetPretrainedModel.pretrained_init_configuration.keys())

    MAPPING_NAMES = OrderedDict([
        # Base model mapping
        (albert, AlbertTokenizer),
        (bart, BartTokenizer),
        (bigbird, BigBirdTokenizer),
        (convbert, ConvBertTokenizer),
        (distilbert, DistilBertTokenizer),
        (electra, ElectraTokenizer),
        (skep, SkepTokenizer),
        (erniectm, ErnieCtmTokenizer),
        (erniedoc, ErnieDocTokenizer),
        (erniegram, ErnieGramTokenizer),
        (ernie, ErnieTokenizer),
        (gpt, GPTTokenizer),
        (mpnet, MPNetTokenizer),
        (nezha, NeZhaTokenizer),
        (roberta, RobertaTokenizer),
        (roformer, RoFormerTokenizer),
        (tinybert, TinyBertTokenizer),
        (bert, BertTokenizer),
        (unifiedtransformer, UnifiedTransformerTokenizer),
        (unimo, UNIMOTokenizer),
        (xlnet, XLNetTokenizer),
    ])
    return MAPPING_NAMES


class AutoTokenizer():
    """
    AutoClass can help you automatically retrieve the relevant model given the provided
    pretrained weights/vocabulary.
    AutoTokenizer is a generic tokenizer class that will be instantiated as one of the
    base tokenizer classes when created with the AutoTokenizer.from_pretrained() classmethod.
    """
    MAPPING_NAMES = get_configurations()
    _tokenizer_mapping = MAPPING_NAMES
    _name_mapping = TOKENIZER_MAPPING_NAMES
    tokenizer_config_file = "tokenizer_config.json"

    def __init__(self, *args, **kwargs):
        raise EnvironmentError(
            f"{self.__class__.__name__} is designed to be instantiated "
            f"using the `{self.__class__.__name__}.from_pretrained(pretrained_model_name_or_path).`"
        )

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, *model_args,
                        **kwargs):
        """
         Creates an instance of `AutoTokenizer`. Related resources are loaded by
         specifying name of a built-in pretrained model, or a community-contributed
         pretrained model, or a local file directory path.

         Args:
             pretrained_model_name_or_path (str): Name of pretrained model or dir path
                 to load from. The string can be:

                 - Name of built-in pretrained model
                 - Name of a community-contributed pretrained model.
                 - Local directory path which contains tokenizer related resources
                   and tokenizer config file ("tokenizer_config.json").
             *args (tuple): position arguments for model `__init__`. If provided,
                 use these as position argument values for tokenizer initialization.
             **kwargs (dict): keyword arguments for model `__init__`. If provided,
                 use these to update pre-defined keyword argument values for tokenizer
                 initialization.

         Returns:
             PretrainedTokenizer: An instance of `PretrainedTokenizer`.

         Example:
             .. code-block::

                 from paddlenlp.transformers import AutoTokenizer

                 # Name of built-in pretrained model
                 tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

                 # Name of community-contributed pretrained model
                 tokenizer = AutoTokenizer.from_pretrained('yingyibiao/bert-base-uncased-sst-2-finetuned')

                 # Load from local directory path
                 tokenizer = AutoTokenizer.from_pretrained('./my_bert/')
         """
        pretrained_model_name_or_path = str(pretrained_model_name_or_path)

        all_tokenizer_names = []
        for names, tokenizer_class in cls._tokenizer_mapping.items():
            for name in names:
                all_tokenizer_names.append(name)

        # From built-in pretrained models
        if pretrained_model_name_or_path in all_tokenizer_names:
            for names, tokenizer_class in cls._tokenizer_mapping.items():
                for pattern in names:
                    if pattern == pretrained_model_name_or_path:
                        return tokenizer_class.from_pretrained(
                            pretrained_model_name_or_path, **kwargs)
        # From local dir path
        elif os.path.isdir(pretrained_model_name_or_path):
            config_file = os.path.join(pretrained_model_name_or_path,
                                       cls.tokenizer_config_file)
            if os.path.exists(config_file):
                with io.open(config_file, encoding="utf-8") as f:
                    init_kwargs = json.load(f)
                # class name corresponds to this configuration
                init_class = init_kwargs.pop("init_class", None)
                if init_class:
                    class_name = cls._name_mapping[init_class]
                    import_class = importlib.import_module(
                        f"paddlenlp.transformers.{class_name}.tokenizer")
                    tokenizer_name = getattr(import_class, init_class)
                    keyerror = False
                    return tokenizer_name.from_pretrained(
                        pretrained_model_name_or_path, *model_args, **kwargs)
                # If no `init_class`, we use pattern recoginition to recoginize the Tokenizer class.
                else:
                    print(
                        'We use pattern recoginition to recoginize the Tokenizer class.'
                    )
                    for key, pattern in cls._name_mapping.items():
                        pretrained_model_name_or_path = pretrained_model_name_or_path.lower(
                        )
                        if pattern in pretrained_model_name_or_path:
                            init_class = key
                            class_name = cls._name_mapping[init_class]
                            import_class = importlib.import_module(
                                f"paddlenlp.transformers.{class_name}.tokenizer")
                            tokenizer_name = getattr(import_class, init_class)
                            print(
                                f"The 'pretrained_model_name_or_path' is {pretrained_model_name_or_path}, we import {tokenizer_name}."
                            )
                            return tokenizer_name.from_pretrained(
                                pretrained_model_name_or_path, *model_args,
                                **kwargs)

        else:
            # Assuming from community-contributed pretrained models
            community_config_path = os.path.join(COMMUNITY_MODEL_PREFIX,
                                                 pretrained_model_name_or_path,
                                                 cls.tokenizer_config_file)

            default_root = os.path.join(MODEL_HOME,
                                        pretrained_model_name_or_path)
            try:
                resolved_vocab_file = get_path_from_url(community_config_path,
                                                        default_root)
                if os.path.exists(resolved_vocab_file):
                    with io.open(resolved_vocab_file, encoding="utf-8") as f:
                        init_kwargs = json.load(f)
                    # class name corresponds to this configuration
                    init_class = init_kwargs.pop("init_class", None)
                    if init_class:
                        class_name = cls._name_mapping[init_class]
                        import_class = importlib.import_module(
                            f"paddlenlp.transformers.{class_name}.tokenizer")
                        tokenizer_name = getattr(import_class, init_class)
                        keyerror = False
                        return tokenizer_name.from_pretrained(
                            pretrained_model_name_or_path, *model_args,
                            **kwargs)
                    # If no `init_class`, we use pattern recoginition to recoginize the Tokenizer class.
                    else:
                        print(
                            'We use pattern recoginition to recoginize the Tokenizer class.'
                        )
                        for key, pattern in cls._name_mapping.items():
                            pretrained_model_name_or_path = pretrained_model_name_or_path.lower(
                            )
                            if pattern in pretrained_model_name_or_path:
                                init_class = key
                                class_name = cls._name_mapping[init_class]
                                import_class = importlib.import_module(
                                    f"paddlenlp.transformers.{class_name}.tokenizer"
                                )
                                tokenizer_name = getattr(import_class,
                                                         init_class)
                                print(
                                    f"The 'pretrained_model_name_or_path' is {pretrained_model_name_or_path}, we import {tokenizer_name}."
                                )
                                return tokenizer_name.from_pretrained(
                                    pretrained_model_name_or_path, *model_args,
                                    **kwargs)
            except RuntimeError as err:
                logger.error(err)
                raise RuntimeError(
                    f"Can't load tokenizer for '{pretrained_model_name_or_path}'.\n"
                    f"Please make sure that '{pretrained_model_name_or_path}' is:\n"
                    "- a correct model-identifier of built-in pretrained models,\n"
                    "- or a correct model-identifier of community-contributed pretrained models,\n"
                    "- or the correct path to a directory containing relevant tokenizer files.\n"
                )
