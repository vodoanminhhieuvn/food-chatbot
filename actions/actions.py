from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.get_entities import ExtractorType, get_entities


class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message(text="Xin chào bạn mình là trợ lý ảo sẽ giúp bạn trong viêc tìm kiếm món ăn")
        # dispatcher.utter_message(
        #     text="Mình có thể hỗ trợ bạn tìm kiếm công thức món ăn dựa trên nguyên liệu, cách nấu ăn và chế độ dinh dưỡng của bạn")

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

        slot_set_list = []

        if not ingredient_entities and not cook_technique_entities:
            dispatcher.utter_message('Mình có thể giúp gì cho bạn ?')

        if cook_technique_entities:
            slot_set_list.append(SlotSet('cook_technique', cook_technique_entities[0]))

        if ingredient_entities:
            if cook_technique_entities:
                slot_set_list.append(SlotSet('cook_technique', cook_technique_entities[0]))

            slot_set_list.append(SlotSet('ingredient_list', ingredient_entities))
            slot_set_list.append(FollowupAction('action_find_recipe'))

        return slot_set_list
