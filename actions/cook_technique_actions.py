from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.get_entities import get_entities
from actions.utils.get_entities import ExtractorType


class ActionSetCookTechnique(Action):
    def name(self) -> Text:
        return "action_set_cook_technique"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        slot_set_list = []

        if cook_technique_entities := get_entities(tracker=tracker, entity='cook_technique',
                                                   extractor=ExtractorType.RegexEntityExtractor):
            slot_set_list.append(SlotSet('cook_technique', None))
            slot_set_list.append(SlotSet('cook_technique', cook_technique_entities[0]))

            ingredient_list = tracker.get_slot('ingredient_list') or get_entities(
                tracker=tracker, entity='cook_technique', extractor=ExtractorType.RegexEntityExtractor) or []

            if ingredient_list:
                # dispatcher.utter_message(f"Hiện tại bạn có nguyên liệu: {' '.join(iter(ingredient_list))}")
                slot_set_list.append(FollowupAction('action_find_recipe'))
            else:
                dispatcher.utter_message('Hiện tại bạn chưa có nguyên liệu nào')
                dispatcher.utter_message(
                    'Bạn hãy cung cấp mình ít nhất 1 nguyên liệu')
                dispatcher.utter_message("Ví dụ: \"Nguyên liệu trứng\" để thêm nguyên liệu trứng")

        else:
            dispatcher.utter_message("Mình biết là bạn muốn cung cấp cách nấu ăn ?")
            dispatcher.utter_message("nhưng mình chưa thấy")
            dispatcher.utter_message("bạn nhập lại dùm mình được không ?")

        return slot_set_list
