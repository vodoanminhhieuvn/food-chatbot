from email import message
from typing import Any, Dict, List, Optional, Text
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.constants import ENTITIES, TEXT

from underthesea import sentiment

# TODO: Correctly register your component with its type


@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR], is_trainable=False
)
class ViSentiment(GraphComponent):
    def __init__(self, config: Dict[Text, Any]) -> None:
        """Initialize SpacyEntityExtractor."""
        self._config = config

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        """Creates a new component (see parent class for full docstring)."""
        return cls(config)

    def convert_to_rasa(self, value, confidence):

        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "sentiment",
                  "extractor": "SentimentExtractor"}

        return entity

    def process(self, messages: List[Message], **kwargs) -> List[Message]:

        for user_message in messages:
            key, confidence = sentiment(user_message.get(TEXT)), 0.5
            entity = self.convert_to_rasa(key, confidence)
            user_message.set("entities", [entity], add_to_output=True)

        return messages
