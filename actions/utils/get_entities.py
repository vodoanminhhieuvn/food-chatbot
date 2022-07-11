from typing import Any, Dict, Text

from rasa_sdk import Tracker


class ExtractorType:
    RegexEntityExtractor: str = 'RegexEntityExtractor'
    DIETClassifier: str = 'DIETClassifier'
    SentimentExtractor: str = 'SentimentExtractor'


def get_entities(
        tracker: Tracker, entity,
        extractor: str = ExtractorType.DIETClassifier) -> Dict[Text, Any]:
    blobs = tracker.latest_message['entities']
    return [blob['value']
            for blob in blobs
            if blob['entity'] == entity and blob['extractor'] == extractor]
