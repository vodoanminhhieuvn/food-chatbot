from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.request.request import request_get_api
from actions.request.http_url import SEARCH_URL
from actions.const.food import PURPOSES

# TODO Tìm kiếm món ăn


class ActionFindRecipe(Action):

    def name(self) -> Text:
        return "action_find_recipe"

    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # step- Check if slot has value or not

        ingredient_list = tracker.get_slot('ingredient_list') or []
        diet_slot = tracker.get_slot('diet') or []
        cook_technique = tracker.get_slot('cook_technique') or ''

        if not ingredient_list and not diet_slot:
            dispatcher.utter_message(
                "Hình như bạn chưa thêm nguyên liệu thì phải ?")
            dispatcher.utter_message(
                'Bạn hãy cung cấp mình ít nhất 1 nguyên liệu')
            dispatcher.utter_message("Bạn có thể thêm nguyên liệu bằng cách nhập: \"Nguyên liệu trứng\" ")

            return []
        # step- Send request API
        url = ''
        for diet in diet_slot:
            for key, value in PURPOSES.items():
                if diet in value:
                    url += f'{key}'
                    break

        params = {
            'q': f"{' '.join(str(ingredient) for ingredient in ingredient_list)} {cook_technique}",
            "page": 1,
            "pageSize": 5,
            "p": url
        }

        response = request_get_api(url=f"{SEARCH_URL}", params=params)

        recipes = response.json()['recipes'][:5]

        seen_recipe = []
        recipes_filter = []

        for recipe in recipes:
            if recipe['Name'].lower() not in seen_recipe:
                print(recipe['Name'])
                seen_recipe.append(recipe['Name'].lower())
                recipes_filter.append(recipe)

        # step- Create button for user to choose
        dispatcher.utter_message(text="Bạn muốn làm món nào ?")

        for hit in recipes_filter:
            dispatcher.utter_message(f"{hit['Name']}")

        if not cook_technique:
            dispatcher.utter_message(f"Vậy bạn có thích kiểu nấu nào không ?")

        return [SlotSet('recipe_search_response', recipes_filter),
                SlotSet('asking_recipe', None),
                SlotSet('previous_search', None)]
