from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.get_entities import get_entities
from actions.utils.get_entities import ExtractorType


class ActionIngredientDetail(Action):
    def name(self) -> Text:
        return "action_ingredient_details"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        ingredient_search = tracker.get_slot('ingredient_search')

        if recipe_index := get_entities(tracker=tracker, entity='detail_index'):
            ingredient_user_need = ingredient_search[int(recipe_index[0])]

        else:
            dispatcher.utter_message("Hình như bạn quên chọn vị trí món ăn")
            return[]

        dispatcher.utter_message(
            json_message={"ingredients": ingredient_user_need}
        )

        return []
