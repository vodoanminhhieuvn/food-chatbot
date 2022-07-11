from rasa_sdk import Tracker


def get_lastest_message(tracker: Tracker,) -> str:
    return tracker.latest_message['text']
