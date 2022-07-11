# from email import message
# from typing import Any, Dict, List, Optional, Text
# from rasa.engine.graph import GraphComponent, ExecutionContext
# from rasa.engine.recipes.default_recipe import DefaultV1Recipe
# from rasa.engine.storage.resource import Resource
# from rasa.engine.storage.storage import ModelStorage
# from rasa.shared.nlu.training_data.message import Message
# from rasa.shared.nlu.training_data.training_data import TrainingData
# from spellchecker import SpellChecker

# spell = SpellChecker()

# # TODO: Correctly register your component with its type


# @DefaultV1Recipe.register(
#     [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER], is_trainable=False
# )
# class SpellChecker(GraphComponent):

#     @classmethod
#     def create(
#         cls,
#         config: Dict[Text, Any],
#         model_storage: ModelStorage,
#         resource: Resource,
#         execution_context: ExecutionContext,
#     ) -> GraphComponent:
#         # TODO: Graph component
#         ...

#     @staticmethod
#     def supported_languages() -> Optional[List[Text]]:
#         return ['en']

#     def train(self, training_data: TrainingData) -> Resource:
#         # TODO: Implement this if your component requires training
#         ...

#     def process_training_data(self, training_data: TrainingData) -> TrainingData:
#         # TODO: Implement this if your component augments the training data with
#         #       tokens or message features which are used by other components
#         #       during training.
#         ...

#         return training_data

#     def process(self, messages: List[Message]) -> List[Message]:
#         new_messages: List[Message]
#         for message in messages:
#             print(message.data)
#             new_messages.push(message)
#         return messages
