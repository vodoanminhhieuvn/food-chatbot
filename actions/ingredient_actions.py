from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.get_entities import get_entities
from actions.utils.get_entities import ExtractorType


class ActionReSetIngredient(Action):
    def name(self) -> Text:
        return "action_re_set_ingredients"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ingredient_entities = get_entities(
            tracker=tracker,
            entity='ingredient',
            extractor=ExtractorType.RegexEntityExtractor
        )

        print(ingredient_entities)

        return [SlotSet('ingredient_list', None), SlotSet('ingredient_list', ingredient_entities), SlotSet('cook_technique', None), FollowupAction('action_find_recipe')]


class ActionSetIngredient(Action):
    def name(self) -> Text:
        return "action_set_ingredients"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        slot_set_list = []

        # step Extracting entities
        ingredient_entities = get_entities(
            tracker=tracker,
            entity='ingredient',
            extractor=ExtractorType.RegexEntityExtractor
        )

        cook_technique_entities = get_entities(
            tracker=tracker,
            entity='cook_technique',
            extractor=ExtractorType.RegexEntityExtractor
        )

        ingredient_list = tracker.get_slot('ingredient_list') or []

        # step Check if contain ingredients or cook technique

        if not ingredient_entities and not cook_technique_entities:
            dispatcher.utter_message("Mình biết là bạn muốn tìm đồ ăn ?")
            dispatcher.utter_message("nhưng mình chưa biết bạn cần gì")
            dispatcher.utter_message("bạn có thể nhập lại cho mình được không  ?")
            return []

        # TODO Handle if user input don't have ingredient only but ingredient already in slot
        if not ingredient_entities:
            dispatcher.utter_message("Hình như bạn chưa cung cấp nguyên liệu nào thì phải ?")
            return []
        else:
            print(ingredient_entities)
            # slot_set_list.append(SlotSet('ingredient_list', None))
            slot_set_list.append(SlotSet('ingredient_list', ingredient_entities))
            # slot_set_list.append(SlotSet('recipe_search_response', None))

        # if cook_technique_entities:
            # slot_set_list.append(SlotSet('cook_technique', None))
            # slot_set_list.append(SlotSet('cook_technique', cook_technique_entities[0]))

        if ingredient_entities:
            slot_set_list.append(FollowupAction('action_find_recipe'))

        return slot_set_list
