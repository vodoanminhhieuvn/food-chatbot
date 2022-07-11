from typing import Any, Dict, List, Optional, Text
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer

from underthesea import word_tokenize


@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER], is_trainable=False
)
class ViTokenizers(Tokenizer):
    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        """Returns the component's default config."""
        return {
            # Flag to check whether to split intents
            "intent_tokenization_flag": False,
            # Symbol on which intent should be split
            "intent_split_symbol": "_",
            # Regular expression to detect tokens
            "token_pattern": None,
        }

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:

        text = message.get(attribute)

        words = word_tokenize(text)

        self._convert_words_to_tokens(words, text)

        tokens = self._convert_words_to_tokens(words, text)

        return self._apply_token_pattern(tokens)
