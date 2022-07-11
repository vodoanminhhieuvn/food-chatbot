from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionSetNutrient(Action):

    def name(self) -> Text:
        return "action_set_nutrient"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        list_nutrient_value = {}

        current_nutrient = ''

        blobs = tracker.latest_message['entities']
        for blob in blobs:
            # step Taking current slot value
            if blob['entity'] == 'nutrient':
                current_nutrient = blob['value']
                list_nutrient_value.update({
                    f'min_{current_nutrient}': tracker.get_slot(f'min_{current_nutrient}'),
                    f'max_{current_nutrient}': tracker.get_slot(f'max_{current_nutrient}')
                })

            # step Checking min_number and swap if needed
            if blob['entity'] == 'min_number':
                if int(blob['value']) > list_nutrient_value[f'max_{current_nutrient}']:
                    list_nutrient_value[f'min_{current_nutrient}'] = list_nutrient_value[f'max_{current_nutrient}']

                    list_nutrient_value[f'max_{current_nutrient}'] = int(blob['value'])
                else:
                    list_nutrient_value[f'min_{current_nutrient}'] = int(blob['value'])

            # step Checking max_number and swap if needed
            if blob['entity'] == 'max_number':
                if int(blob['value']) < list_nutrient_value[f'min_{current_nutrient}']:
                    list_nutrient_value[f'max_{current_nutrient}'] = list_nutrient_value[f'max_{current_nutrient}']

                    list_nutrient_value[f'min_{current_nutrient}'] = int(blob['value'])
                else:
                    list_nutrient_value[f'max_{current_nutrient}'] = int(blob['value'])

        nutrient_messages = "".join(
            f"{key}:  {value}\n"
            for key, value in list_nutrient_value.items()
        )

        dispatcher.utter_message(nutrient_messages)

        return [SlotSet(slot_name, slot_value) for slot_name, slot_value in list_nutrient_value.items()]
