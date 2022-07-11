from typing import Text, Dict, Any, List
from numpy import disp

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.get_entities import get_entities
from actions.utils.get_entities import ExtractorType
from actions.request.http_url import GET_DETAIL_URL
from actions.request.request import request_get_api
from actions.modules.remove_accents import compare_ascii_string

from underthesea import word_tokenize
import jellyfish


def show_recipe_detail(recipe_user_need, dispatcher: CollectingDispatcher):
    print('---------------')
    print(recipe_user_need['Id'])
    response = request_get_api(url=f"{GET_DETAIL_URL}{recipe_user_need['Id']}")
    recipe_data = response.json()['data']

    ingredient_messages = "".join(
        f"{ingredient['name']} \n"
        for ingredient in recipe_data['ingredients']
    )

    dispatcher.utter_message(recipe_user_need['Name'])
    dispatcher.utter_message(image=recipe_user_need['Img'])
    dispatcher.utter_message(f"Tổng thời gian: {recipe_data['totalTime']} phút")
    dispatcher.utter_message(ingredient_messages)
    dispatcher.utter_custom_json(json_message={'youtubeId': recipe_user_need['Video']})


class ActionHowToCook(Action):
    def name(self) -> Text:
        return "action_how_to_cook"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        try:
            recipe_hits = tracker.get_slot('recipe_search_response')
            asking_recipe_before = tracker.get_slot('asking_recipe') or False
            # _ Tokenize user message input
            user_message_tokenizer = word_tokenize(tracker.latest_message.get('text'))

            food_rating_token = []

            for index, recipe in enumerate(recipe_hits):
                print(recipe['Name'])
                for word in user_message_tokenizer:
                    if compare_ascii_string(word.lower(), recipe["Name"].lower())[0]:
                        try:
                            if word.lower() not in food_rating_token[index]:
                                food_rating_token[index].append(word)
                        except IndexError:
                            food_rating_token.append([word])

                    if word == user_message_tokenizer[-1]:
                        try:
                            food_rating_token[index]
                        except IndexError:
                            food_rating_token.append([])

            food_rating_score = []

            for food_token in food_rating_token:
                food_rating_score.append(len(food_token))

            max_score = max(food_rating_score)

            list_highest_score = [i for i, j in enumerate(food_rating_score) if j == max_score]
            print('----------------+-------------------')

            print(f"total search: {len(recipe_hits)}")
            print(food_rating_score)
            print(f'Lengt: {len(list_highest_score)}')
            print(list_highest_score)

            if len(list_highest_score) > 1:
                # # If there are more than one recipe with the same score, we will show the list of recipe
                if not asking_recipe_before:
                    dispatcher.utter_message('Ý bạn là món nào trong đây nhỉ ??')
                    for index in list_highest_score:
                        dispatcher.utter_message(recipe_hits[index]['Name'])
                    return [SlotSet('asking_recipe', True), SlotSet('previous_search', list_highest_score)]
                else:
                    previous_search = tracker.get_slot('previous_search') or []
                    highest_similarity_score = -99999
                    # # Check similarity between user message and recipe name
                    for index in previous_search:
                        if jellyfish.jaro_winkler_similarity(
                                recipe_hits[index]['Name'].lower(),
                                tracker.latest_message.get('text').lower()
                        ) > highest_similarity_score:
                            highest_similarity_score = jellyfish.jaro_winkler(
                                recipe_hits[index]['Name'],
                                tracker.latest_message.get('text')
                            )
                            highest_similarity = recipe_hits[index]

                    show_recipe_detail(highest_similarity, dispatcher)

                    return [SlotSet('asking_recipe', None), SlotSet('previous_search', None)]
                    # show_recipe_detail(recipe_hits[list_highest_score[0]], dispatcher)
            else:
                show_recipe_detail(recipe_hits[list_highest_score[0]], dispatcher)

        except TypeError:
            ingredient_list = tracker.get_slot('ingredient_list') or []
            cook_technique_list = tracker.get_slot('cook_technique') or []
            if ingredient_list != []:
                dispatcher.utter_message(f"Nguyên liệu hiện tài của bạn: {' '.join(iter(ingredient_list))}")

            else:
                dispatcher.utter_message("Bạn chưa có nguyên liệu nào")
                dispatcher.utter_message("Bạn có thể thêm nguyên liệu bằng cách nhập: \"Nguyên liệu trứng\" ")

            if cook_technique_list != []:
                dispatcher.utter_message(f"Cách nấu hiện tài của bạn: {cook_technique_list}")
            else:
                dispatcher.utter_message("Bạn chưa có cách nấu nào")
                dispatcher.utter_message("Bạn có thể thêm cách nấu bằng cách nhập: \"Mình muốn chiên\" ")

            if ingredient_list != []:
                dispatcher.utter_message("Nhắn \"tìm món ăn\" để tìm các món ăn phù hợp với nguyên liệu của bạn")

        return []
