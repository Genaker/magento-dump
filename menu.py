from simple_term_menu import TerminalMenu
from db_config import get_db_config_from_env
from table_utils import list_large_tables
from dump_utils import perform_db_dump
import argparse

def execute_command(command):
    """Execute the command either via CLI arguments or interactive menu."""
    config = get_db_config_from_env()

    if command == "show-tables":
        list_large_tables(config)
    elif command == "db-dump":
        perform_db_dump(config)
    else:
        show_commands()

def show_commands():
    """Interactive menu with descriptions."""
    menu_options = [
        "📋 Show Large Tables  → List only tables > 1MB with row counts & sizes",
        "💾 Dump All Tables    → Create a full database dump (gzip compressed)",
        "❌ Exit               → Quit the tool"
    ]
    
    menu = TerminalMenu(menu_options, title="🔧 Magento Database Tool - Select an Option", menu_cursor="👉 ")
    selection = menu.show()

    if selection == 0:
        execute_command("show-tables")
    elif selection == 1:
        execute_command("db-dump")
    else:
        print("👋 Exiting. Have a great day!")
        exit()
