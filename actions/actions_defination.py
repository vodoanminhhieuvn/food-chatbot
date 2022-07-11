from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.data.definations import get_defination_data, valid_defination
from actions.utils.get_entities import get_entities


class ActionDefination(Action):

    def name(self) -> Text:
        return "action_defination"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        list_defination_entities = get_entities(
            tracker=tracker, entity='defination')

        for defination in list_defination_entities:
            if valid_defination(defination):
                for text in get_defination_data(defination):
                    dispatcher.utter_message(text,
                                             buttons=[{"payload": "/affirm", "title": "Yes"},
                                                      {"payload": "/deny", "title": "No"}, ])

        dispatcher.utter_message(buttons=[{"payload": "/affirm", "title": "Yes"},
                                          {"payload": "/deny", "title": "No"}, ])

        return []
