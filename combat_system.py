"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Silas Hayes

AI Usage: [Document any AI assistance used]

Handles combat mechanics
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

    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward

def get_random_enemy_for_level(character_level):
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn = 1
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        
    
    def start_battle(self):
        if self.character["health"] <= 0:
            raise CharacterDeadError("Character is already dead.")

        while self.combat_active:
            display_combat_stats(self.character, self.enemy)

            self.player_turn()
            result = self.check_battle_end()
            if result:
                return result

            self.enemy_turn()
            result = self.check_battle_end()
            if result:
                return result
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        
    
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

        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        
    
    def enemy_turn(self):
        if not self.combat_active:
            raise CombatNotActiveError()

        print("\n--- ENEMY TURN ---")
        dmg = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, dmg)
        display_battle_log(f"{self.enemy['name']} hits you for {dmg} damage!")
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        
    
    def calculate_damage(self, attacker, defender):
         dmg = attacker["strength"] - (defender["strength"] // 4)
         return max(1, dmg)
        # TODO: Implement damage calculation
        
    
    def apply_damage(self, target, damage):
        target["health"] = max(0, target["health"] - damage)
        
        # TODO: Implement damage application
        
    
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

        # TODO: Implement battle end check
        
    
    def attempt_escape(self):
        success = random.random() < 0.5
        if success:
            self.combat_active = False
        return success

        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        

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
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    

def warrior_power_strike(character, enemy):
    dmg = character["strength"] * 2
    enemy["health"] -= dmg
    return f"Power Strike! You dealt {dmg} damage."

    # TODO: Implement power strike
    # Double strength damage
    

def mage_fireball(character, enemy):
    dmg = character["magic"] * 2
    enemy["health"] -= dmg
    return f"Fireball! You dealt {dmg} magic damage."

    # TODO: Implement fireball
    # Double magic damage
    

def rogue_critical_strike(character, enemy):
    if random.random() < 0.5:
        dmg = character["strength"] * 3
        enemy["health"] -= dmg
        return f"Critical Strike! Triple damage ({dmg})!"
    else:
        dmg = character["strength"]
        enemy["health"] -= dmg
        return f"Critical failed. You deal normal damage ({dmg})."

    # TODO: Implement critical strike
    # 50% chance for triple damage
    

def cleric_heal(character):
    heal = 30
    character["health"] = min(character["max_health"], character["health"] + heal)
    return f"You heal yourself for {heal} HP."
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)


# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    return character["health"] > 0

    # TODO: Implement fight check
    

def get_victory_rewards(enemy):
    return {
        "xp": enemy["xp_reward"],
        "gold": enemy["gold_reward"]
    }

    # TODO: Implement reward calculation
     

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")


# ============================================================================
# TESTING
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
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

