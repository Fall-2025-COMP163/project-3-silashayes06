"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Completed Implementation

Name: Silas Hayes

AI Usage: Assisted with any indentation or syntax errors that I orignially did not notice.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """Display main menu and get player choice"""
    while True:
        print("\n=== MAIN MENU ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")
        choice = input("Enter choice (1-3): ").strip()
        if choice in ('1', '2', '3'):
            return int(choice)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def new_game():
    """Start a new game"""
    global current_character
    while True:
        name = input("Enter your character name: ").strip()
        char_class = input("Enter your character class: ").strip()
        try:
            current_character = character_manager.create_character(name, char_class)
            character_manager.save_character(current_character)
            print(f"Character {name} the {char_class} created successfully!")
            game_loop()
            break
        except InvalidCharacterClassError:
            print("Invalid class. Please choose again.")

def load_game():
    """Load an existing saved game"""
    global current_character
    saved_characters = character_manager.list_saved_characters()
    if not saved_characters:
        print("No saved characters found. Start a new game.")
        return
    print("\nSaved Characters:")
    for i, char_name in enumerate(saved_characters, 1):
        print(f"{i}. {char_name}")
    while True:
        choice = input(f"Select a character (1-{len(saved_characters)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(saved_characters):
            try:
                current_character = character_manager.load_character(saved_characters[int(choice) - 1])
                print(f"Character {current_character['name']} loaded successfully!")
                game_loop()
                break
            except (CharacterNotFoundError, SaveFileCorruptedError) as e:
                print(f"Error loading character: {e}")
                break
        else:
            print("Invalid choice. Try again.")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """Main game loop"""
    global game_running
    game_running = True
    while game_running:
        choice = game_menu()
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Goodbye!")
            game_running = False
        else:
            print("Invalid choice.")

def game_menu():
    """Display game menu and get player choice"""
    while True:
        print("\n=== GAME MENU ===")
        print("1. View Character Stats")
        print("2. View Inventory")
        print("3. Quest Menu")
        print("4. Explore")
        print("5. Shop")
        print("6. Save and Quit")
        choice = input("Enter choice (1-6): ").strip()
        if choice in ('1','2','3','4','5','6'):
            return int(choice)
        else:
            print("Invalid input. Enter 1-6.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    character_manager.display_character_info(current_character)
    quest_handler.display_character_quest_progress(current_character, all_quests)

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    while True:
        inventory_system.display_inventory(current_character, all_items)
        print("Options:")
        print("1. Use Item")
        print("2. Equip Weapon")
        print("3. Equip Armor")
        print("4. Drop Item")
        print("5. Back")
        choice = input("Enter choice: ").strip()
        try:
            if choice == '1':
                item_id = input("Enter item ID to use: ").strip()
                inventory_system.use_item(current_character, item_id, all_items[item_id])
            elif choice == '2':
                item_id = input("Enter weapon ID to equip: ").strip()
                inventory_system.equip_weapon(current_character, item_id, all_items[item_id])
            elif choice == '3':
                item_id = input("Enter armor ID to equip: ").strip()
                inventory_system.equip_armor(current_character, item_id, all_items[item_id])
            elif choice == '4':
                item_id = input("Enter item ID to drop: ").strip()
                inventory_system.remove_item_from_inventory(current_character, item_id)
            elif choice == '5':
                break
            else:
                print("Invalid choice.")
        except (ItemNotFoundError, InventoryFullError, InvalidItemTypeError) as e:
            print(f"Error: {e}")

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    while True:
        print("\n=== QUEST MENU ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest")
        print("7. Back")
        choice = input("Enter choice: ").strip()
        try:
            if choice == '1':
                active = quest_handler.get_active_quests(current_character, all_quests)
                quest_handler.display_quest_list(active)
            elif choice == '2':
                available = quest_handler.get_available_quests(current_character, all_quests)
                quest_handler.display_quest_list(available)
            elif choice == '3':
                completed = quest_handler.get_completed_quests(current_character, all_quests)
                quest_handler.display_quest_list(completed)
            elif choice == '4':
                quest_id = input("Enter quest ID to accept: ").strip()
                quest_handler.accept_quest(current_character, quest_id, all_quests)
                print(f"Quest {quest_id} accepted!")
            elif choice == '5':
                quest_id = input("Enter quest ID to abandon: ").strip()
                quest_handler.abandon_quest(current_character, quest_id)
                print(f"Quest {quest_id} abandoned.")
            elif choice == '6':
                quest_id = input("Enter quest ID to complete: ").strip()
                rewards = quest_handler.complete_quest(current_character, quest_id, all_quests)
                print(f"Quest {quest_id} completed! Rewards: {rewards}")
            elif choice == '7':
                break
            else:
                print("Invalid choice.")
        except (QuestError, QuestNotFoundError, QuestNotActiveError, QuestRequirementsNotMetError) as e:
            print(f"Error: {e}")

def explore():
    """Find and fight random enemies"""
    global current_character
    enemy = combat_system.generate_random_enemy(current_character['level'])
    print(f"Encountered {enemy['name']}!")
    try:
        result = combat_system.SimpleBattle(current_character, enemy)
        print(f"Battle Result: {result}")
        if current_character['health'] <= 0:
            handle_character_death()
    except CombatError as e:
        print(f"Combat error: {e}")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    while True:
        print(f"Gold: {current_character['gold']}")
        print("Available items:")
        for item_id, data in all_items.items():
            print(f"{item_id}: {data['type']} - Cost: {data.get('cost',0)}")
        print("Options:")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Back")
        choice = input("Enter choice: ").strip()
        try:
            if choice == '1':
                item_id = input("Enter item ID to buy: ").strip()
                inventory_system.purchase_item(current_character, item_id, all_items[item_id])
            elif choice == '2':
                item_id = input("Enter item ID to sell: ").strip()
                gold_received = inventory_system.sell_item(current_character, item_id, all_items[item_id])
                print(f"Sold for {gold_received} gold.")
            elif choice == '3':
                break
            else:
                print("Invalid choice.")
        except (InventoryFullError, InsufficientResourcesError, ItemNotFoundError) as e:
            print(f"Error: {e}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    try:
        character_manager.save_character(current_character)
        print("Game saved successfully!")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Game data files missing. Creating defaults...")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except InvalidDataFormatError as e:
        print(f"Invalid data format: {e}")
        raise

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    print("You have died!")
    while True:
        choice = input("1. Revive (costs gold) 2. Quit: ").strip()
        if choice == '1':
            try:
                character_manager.revive_character(current_character)
                print("You have been revived!")
                break
            except InsufficientResourcesError:
                print("Not enough gold to revive!")
        elif choice == '2':
            print("Game Over.")
            game_running = False
            break
        else:
            print("Invalid choice.")

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    display_welcome()
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except (MissingDataFileError, InvalidDataFormatError):
        print("Error loading game data.")
        return

    while True:
        choice = main_menu()
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()


