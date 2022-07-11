from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.const.cook_technique import COOK_TECHNIQUE_DESCRIPTION


class ActionClearConfig(Action):
    def name(self) -> Text:
        return "action_clear_config"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            'Mình đã xoá lịch sữ tìm kiếm của bạn')

        return [SlotSet('recipe_search_response', None),
                SlotSet('asking_recipe', None),
                SlotSet('previous_search', None),
                SlotSet('ingredient_list', None),
                SlotSet('cuisine', None),
                SlotSet('cook_technique', None),
                SlotSet('food_search_query', None),
                SlotSet('diet', None), ]
