"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Full Implementation

Name: Silas Hayes

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    if not os.path.exists(filename):
        raise MissingDataFileError(f"{filename} not found")

    try:
        with open(filename, "r") as f:
            content = f.read()
    except Exception:
        raise CorruptedDataError(f"Cannot read {filename}")

    quests = {}
    blocks = content.strip().split("\n\n")
    for block in blocks:
        try:
            quest = parse_quest_block(block.splitlines())
            validate_quest_data(quest)
            quests[quest["quest_id"]] = quest
        except InvalidDataFormatError as e:
            raise InvalidDataFormatError(f"In {filename}: {e}")

    return quests

def load_items(filename="data/items.txt"):
    if not os.path.exists(filename):
        raise MissingDataFileError(f"{filename} not found")

    try:
        with open(filename, "r") as f:
            content = f.read()
    except Exception:
        raise CorruptedDataError(f"Cannot read {filename}")

    items = {}
    blocks = content.strip().split("\n\n")
    for block in blocks:
        try:
            item = parse_item_block(block.splitlines())
            validate_item_data(item)
            items[item["item_id"]] = item
        except InvalidDataFormatError as e:
            raise InvalidDataFormatError(f"In {filename}: {e}")

    return items

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_data(quest_dict):
    required_fields = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold", "required_level", "prerequisite"
    ]
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing field: {field}")

    numeric_fields = ["reward_xp", "reward_gold", "required_level"]
    for field in numeric_fields:
        try:
            quest_dict[field] = int(quest_dict[field])
        except Exception:
            raise InvalidDataFormatError(f"{field} must be an integer")

    return True

def validate_item_data(item_dict):
    required_fields = ["item_id", "name", "type", "effect", "cost", "description"]
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing field: {field}")

    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    try:
        item_dict["cost"] = int(item_dict["cost"])
    except Exception:
        raise InvalidDataFormatError("Cost must be an integer")

    return True

# ============================================================================
# DEFAULT DATA FILES
# ============================================================================

def create_default_data_files():
    os.makedirs("data", exist_ok=True)

    quests_file = "data/quests.txt"
    if not os.path.exists(quests_file):
        default_quests = """QUEST_ID: first_quest
TITLE: A New Beginning
DESCRIPTION: Begin your adventure.
REWARD_XP: 100
REWARD_GOLD: 50
REQUIRED_LEVEL: 1
PREREQUISITE: NONE
"""
        with open(quests_file, "w") as f:
            f.write(default_quests)

    items_file = "data/items.txt"
    if not os.path.exists(items_file):
        default_items = """ITEM_ID: potion_small
NAME: Small Healing Potion
TYPE: consumable
EFFECT: health:20
COST: 50
DESCRIPTION: Restores 20 HP.
"""
        with open(items_file, "w") as f:
            f.write(default_items)

# ============================================================================
# PARSING HELPERS
# ============================================================================

def parse_quest_block(lines):
    quest = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Invalid line: {line}")
        key, value = line.split(": ", 1)
        quest[key.lower()] = value
    quest["quest_id"] = quest.pop("quest_id")
    quest["title"] = quest.pop("title")
    quest["description"] = quest.pop("description")
    quest["reward_xp"] = quest.pop("reward_xp")
    quest["reward_gold"] = quest.pop("reward_gold")
    quest["required_level"] = quest.pop("required_level")
    quest["prerequisite"] = quest.pop("prerequisite")
    return quest

def parse_item_block(lines):
    item = {}
    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError(f"Invalid line: {line}")
        key, value = line.split(": ", 1)
        item[key.lower()] = value
    item["item_id"] = item.pop("item_id")
    item["name"] = item.pop("name")
    item["type"] = item.pop("type")
    item["effect"] = item.pop("effect")
    item["cost"] = item.pop("cost")
    item["description"] = item.pop("description")
    return item

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    create_default_data_files()
    quests = load_quests()
    items = load_items()
    print(f"Loaded {len(quests)} quests and {len(items)} items")



