from dataclasses import dataclass
from enum import Enum
from xmlrpc.client import Boolean, boolean
from dacite import from_dict
import json
from typing import List


Definations = ["oop", "classes", "objects", "abstracts"]

definations_data = {}

with open('./actions/data/definations.json') as f:
    definations_data = json.load(f)


def valid_defination(defination: str) -> Boolean:
    return defination in Definations


def get_defination_data(defination: str):
    return definations_data[defination]
