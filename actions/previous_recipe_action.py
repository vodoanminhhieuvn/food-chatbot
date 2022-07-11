from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.get_entities import get_entities
from actions.utils.get_entities import ExtractorType


class ActionPreviousRecipe(Action):
    def name(self) -> Text:
        return "action_previous_recipe"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        recipe_hits = tracker.get_slot('recipe_search_response')

        if not recipe_hits:
            dispatcher.utter_message("Bạn chưa có tìm món nào :<")
            return []

        buttons = [{"title": f"{index}-{hit['Name']}", "payload": f"chế biến món {index}"}
                   for index, hit in enumerate(recipe_hits['recipes'])]

        dispatcher.utter_message(buttons=buttons)

        return []
