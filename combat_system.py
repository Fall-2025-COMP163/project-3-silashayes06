"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Fixed Version

Name: Silas Hayes

AI Usage: Corrected code formatting, exception handling, and main test block.
"""

import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================ 
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    enemy_type = enemy_type.lower()

    enemies = {
        "goblin":  {"health": 50,  "strength": 8,  "magic": 2,  "xp_reward": 25,  "gold_reward": 10},
        "orc":     {"health": 80,  "strength": 12, "magic": 5,  "xp_reward": 50,  "gold_reward": 25},
        "dragon":  {"health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100},
    }

    if enemy_type not in enemies:
        raise InvalidTargetError(f"Invalid enemy type: {enemy_type}")

    base = enemies[enemy_type]

    return {
        "name": enemy_type.capitalize(),
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "xp_reward": base["xp_reward"],
        "gold_reward": base["gold_reward"]
    }

def get_random_enemy_for_level(character_level):
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

# ============================================================================ 
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    """

    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn = 1

    def start_battle(self):
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character is already dead.")

        while self.combat_active:
            display_combat_stats(self.character, self.enemy)

            result = self.player_turn()
            if result:
                return result

            self.enemy_turn()
            result = self.check_battle_end()
            if result:
                return result

    def player_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError()

        print("\n--- PLAYER TURN ---")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Run")

        choice = input("Choose: ").strip()

        if choice == "1":
            dmg = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, dmg)
            display_battle_log(f"You hit the {self.enemy['name']} for {dmg} damage.")

        elif choice == "2":
            msg = use_special_ability(self.character, self.enemy)
            display_battle_log(msg)

        elif choice == "3":
            if self.attempt_escape():
                display_battle_log("You successfully escaped!")
                return {"winner": "escape", "xp_gained": 0, "gold_gained": 0}
            else:
                display_battle_log("You failed to escape!")

        else:
            display_battle_log("Invalid choice. Turn skipped.")

    def enemy_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError()

        print("\n--- ENEMY TURN ---")
        dmg = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, dmg)
        display_battle_log(f"{self.enemy['name']} hits you for {dmg} damage!")

    def calculate_damage(self, attacker, defender):
        dmg = attacker["strength"] - (defender["strength"] // 4)
        return max(1, dmg)

    def apply_damage(self, target, damage):
        target["health"] = max(0, target["health"] - damage)

    def check_battle_end(self):
        if self.enemy["health"] <= 0:
            rewards = get_victory_rewards(self.enemy)
            self.character["experience"] += rewards["xp"]
            self.character["gold"] += rewards["gold"]
            self.combat_active = False
            display_battle_log("You defeated the enemy!")
            return {"winner": "player", **rewards}

        if self.character["health"] <= 0:
            self.combat_active = False
            display_battle_log("You were defeated...")
            return {"winner": "enemy", "xp_gained": 0, "gold_gained": 0}

        return None

    def attempt_escape(self):
        success = random.random() < 0.5
        if success:
            self.combat_active = False
        return success

# ============================================================================ 
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    cls = character["class"]

    if cls == "Warrior":
        return warrior_power_strike(character, enemy)
    elif cls == "Mage":
        return mage_fireball(character, enemy)
    elif cls == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif cls == "Cleric":
        return cleric_heal(character)
    else:
        return "Your class has no special ability."

def warrior_power_strike(character, enemy):
    dmg = character["strength"] * 2
    enemy["health"] = max(0, enemy["health"] - dmg)
    return f"Power Strike! You dealt {dmg} damage."

def mage_fireball(character, enemy):
    dmg = character["magic"] * 2
    enemy["health"] = max(0, enemy["health"] - dmg)
    return f"Fireball! You dealt {dmg} magic damage."

def rogue_critical_strike(character, enemy):
    if random.random() < 0.5:
        dmg = character["strength"] * 3
        enemy["health"] = max(0, enemy["health"] - dmg)
        return f"Critical Strike! Triple damage ({dmg})!"
    else:
        dmg = character["strength"]
        enemy["health"] = max(0, enemy["health"] - dmg)
        return f"Critical failed. You deal normal damage ({dmg})."

def cleric_heal(character):
    heal = 30
    character["health"] = min(character["max_health"], character["health"] + heal)
    return f"You heal yourself for {heal} HP."

# ============================================================================ 
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    return character["health"] > 0

def get_victory_rewards(enemy):
    return {
        "xp": enemy["xp_reward"],
        "gold": enemy["gold_reward"]
    }

def display_combat_stats(character, enemy):
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")

def display_battle_log(message):
    print(f">>> {message}")

# ============================================================================ 
# MAIN TEST BLOCK
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")

    test_char = {
        "name": "Hero",
        "class": "Warrior",
        "health": 120,
        "max_health": 120,
        "strength": 15,
        "magic": 5,
        "experience": 0,
        "gold": 0
    }

    enemy = create_enemy("goblin")
    battle = SimpleBattle(test_char, enemy)
    result = battle.start_battle()
    print("RESULT:", result)

