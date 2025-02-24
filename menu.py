from simple_term_menu import TerminalMenu
from db_config import get_db_config_from_env
from table_utils import list_large_tables
from db_dump_utils import perform_db_dump
from code_dump_utils import dump_magento_code, dump_magento_media
import argparse

def execute_command(command):
    """Execute the command either via CLI arguments or interactive menu."""
    config = get_db_config_from_env()

    if command == "show-tables":
        list_large_tables(config)
    elif command == "db-dump":
        perform_db_dump(config)
    elif command == "code-dump":
        dump_magento_code() # Archive Magento codebase excluding media/cache
    elif command == "media-dump":
        dump_magento_media() # Archive Magento media excluding media/cache
    else:
        show_commands()

def show_commands():
    """Interactive menu with descriptions."""
    menu_options = [
        "📋 Show Large Tables  → List only tables > 1MB with row counts & sizes",
        "💾 Dump All Tables    → Create a full database dump (gzip compressed)",
        "🗃 Dump Magento Code  → Archive Magento codebase excluding media/cache",
        "🗃 Dump Magento Media  → Archive Magento media excluding media/cache",
        "❌ Exit               → Quit the tool"
    ]
    
    menu = TerminalMenu(menu_options, title="🔧 Magento Database Tool - Select an Option", menu_cursor="👉 ")
    selection = menu.show()

    if selection == 0:
        execute_command("show-tables")
    elif selection == 1:
        execute_command("db-dump")
    elif selection == 2:
        execute_command("code-dump")
    elif selection == 3:
        execute_command("media-dump")
    else:
        print("👋 Exiting. Have a great day!")
        exit()
