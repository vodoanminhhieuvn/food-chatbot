from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.get_entities import get_entities
from actions.const.food import PURPOSES


class ActionSetDiet(Action):

    def name(self) -> Text:
        return "action_set_diet"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        list_diet = get_entities(tracker=tracker, entity='diet')

        # message = "".join(
        #     f"{diet} \n"
        #     for diet in list_diet
        # )

        dispatcher.utter_message(f"Chế độ ăn hiện tại của bạn: {' '.join(iter(list_diet))}")
        # dispatcher.utter_message("Nhắn \"tìm món ăn\" để tìm các món ăn phù hợp với chế độ ăn của bạn")

        return [SlotSet('diet', list_diet), FollowupAction('action_find_recipe')]
