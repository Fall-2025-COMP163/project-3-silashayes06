"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Silas Hayes

AI Usage: ChatGPT was used to fix any and all indentation errors, as well as providing understanding to things I was confused on

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15}
    }
    if character_class not in valid_classes:
        raise InvalidCharacterClassError("Invalid class")
    base = valid_classes[character_class]
    return {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list

def save_character(character, save_directory="data/save_games"):
    os.makedirs(save_directory, exist_ok=True)

    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filename, "w") as f:
            for key, value in character.items():
                if isinstance(value, list):
                    value = ",".join(map(str, value))
                f.write(f"{key.upper()}: {value}\n")

        return True

    except Exception:
        raise
#ChatGPT formatted this line of code with the correct indentation, since it wouldn't have worked the way it was originally formatted. 
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values

def load_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError("Character not found")

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except Exception:
        raise SaveFileCorruptedError("Cannot read save file")

    character = {}
    required_fields = [
        "NAME", "CLASS", "LEVEL", "HEALTH", "MAX_HEALTH",
        "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD",
        "INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"
    ]

    for line in lines:
        if ":" not in line:
            raise InvalidSaveDataError("Invalid save format")
        key, value = line.strip().split(":", 1)
        value = value.strip()
        character[key.lower()] = value

    for field in required_fields:
        if field.lower() not in character:
            raise InvalidSaveDataError("Missing required field")

    try:
        character["level"] = int(character["level"])
        character["health"] = int(character["health"])
        character["max_health"] = int(character["max_health"])
        character["strength"] = int(character["strength"])
        character["magic"] = int(character["magic"])
        character["experience"] = int(character["experience"])
        character["gold"] = int(character["gold"])
        character["inventory"] = character["inventory"].split(",") if character["inventory"] else []
        character["active_quests"] = character["active_quests"].split(",") if character["active_quests"] else []
        character["completed_quests"] = character["completed_quests"].split(",") if character["completed_quests"] else []
    except Exception:
        raise InvalidSaveDataError("Incorrect data types")

    return character


    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists

def list_saved_characters(save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        return []

    files = os.listdir(save_directory)
    return [f.replace("_save.txt", "") for f in files if f.endswith("_save.txt")]
    
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames

def delete_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.exists(filename):
        raise CharacterNotFoundError("Character does not exist")

    os.remove(filename)
    return True
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion


# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    if character["health"] <= 0:
        raise CharacterDeadError("Cannot gain XP while dead")

    character["experience"] += xp_amount

    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

    return character
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up

def add_gold(character, amount):
    if character["gold"] + amount < 0:
        raise ValueError("Gold cannot be negative")

    character["gold"] += amount
    return character["gold"]
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold

def heal_character(character, amount):
    old_health = character["health"]
    character["health"] = min(character["health"] + amount, character["max_health"])
    return character["health"] - old_health
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    

def is_character_dead(character):
    return character["health"] <= 0
    # TODO: Implement death check

def revive_character(character):
    if character["health"] > 0:
        return False

    character["health"] = character["max_health"] // 2
    return True
    # TODO: Implement revival
    # Restore health to half of max_health
# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    required = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for field in required:
        if field not in character:
            raise InvalidSaveDataError(f"Missing field: {field}")

    numeric_fields = [
        "level", "health", "max_health", "strength",
        "magic", "experience", "gold"
    ]

    for field in numeric_fields:
        if not isinstance(character[field], int):
            raise InvalidSaveDataError(f"Invalid type for {field}")

    list_fields = ["inventory", "active_quests", "completed_quests"]
    for field in list_fields:
        if not isinstance(character[field], list):
            raise InvalidSaveDataError(f"Invalid type for {field}")

    return True
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

