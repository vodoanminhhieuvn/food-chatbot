from typing import Any, Dict, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import FollowupAction

FALLBACK_ACTION = {
    "ask_for_nutrient": {"message": "ingredient thì phải ?"},
    "ask_for_create_meal_plan": {"message": "tạo thực đơn"},
    "ask_what_is_cook_technique": {"message": "hỏi cách nấu là gì"},
    "set_ingredients": {"message": "cung cấp nguyên liệu nấu ăn"},
    "ask_what_ingredients": {"message": "hỏi nguyên liệu nấu ăn"},
    "ask_find_recipe": {"message": "tìm công thức nấu ăn"},
    "ask_how_to_cook": {"message": "xem cách chế biến"},
    "ask_ingredient_details": {"message": "xem nguyên liệu chế biến"},
    "provide_cook_technique": {"message": "cung cấp cách nấu ăn"}
}


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]):
        # output a message saying that the conversation will now be
        # continued by a human.

        list_possible_intent = []

        print(tracker.latest_message['intent_ranking'])

        # _ Step 1: Extracting actions probilities
        for intent in tracker.latest_message['intent_ranking']:
            if intent['confidence'] > 0.5:
                if intent['name'] != 'out_of_scope' and intent['name'] != 'nlu_fallback':
                    list_possible_intent.append(intent['name'])

        print('Fallback')

        # _ Step 2: Get more than 50% probability of action_default_fallback

        if list_possible_intent[0] == 'ask_how_to_cook':
            return [FollowupAction('action_how_to_cook')]

        if list_possible_intent[0] == 'greet':
            return [FollowupAction('action_greet')]

        if list_possible_intent[0] == 'set_ingredient':
            return [FollowupAction('action_set_ingredient')]

        if list_possible_intent[0] == 're_set_ingredients':
            return [FollowupAction('action_re_set_ingredients')]

        return []
