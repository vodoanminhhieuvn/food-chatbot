from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.get_entities import get_entities

# TODO Đưa thông tin chi tiết món ăn


class ActionRecipeDetail(Action):

    def name(self) -> Text:
        return "action_recipe_detail"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # step -Get entities from slots and message
        recipe_hits = tracker.get_slot('recipe_search_response')['hits']

        if recipe_index := get_entities(tracker=tracker, entity='detail_index'):
            recipe_user_need = recipe_hits[int(recipe_index[0])]['recipe']

        else:
            dispatcher.utter_message("Seem like you missing position of food")
            return[]

        nutrient_messages = "".join(
            f"{nutrient['label']} - {int(nutrient['quantity']) / int(recipe_user_need['yield'])} \n"
            for nutrient in recipe_user_need['totalNutrients'].values()
        )

        # step -Create button for user to choose recipe

        # ingredient_buttons = [{"title": f"{index}- {ingredient}", "payload": f"ingredient detail {index}"}
        #                       for index, ingredient in enumerate(recipe_user_need['ingredientLines'])]

        # step -Show recipe detail
        dispatcher.utter_message(image=recipe_user_need['images']['SMALL']['url'])
        dispatcher.utter_message(f"Diet-label: {recipe_user_need['dietLabels']}")
        dispatcher.utter_message(nutrient_messages)
        dispatcher.utter_message(buttons=[{
            "title": f"how to cook {recipe_index[0]}",
            "payload": f"how to cook {recipe_index[0]}"
        }])

        return []
