from simple_term_menu import TerminalMenu
from db_config import get_db_config_from_env
from table_utils import list_large_tables
from dump_utils import perform_db_dump

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
        config = get_db_config_from_env()
        list_large_tables(config)
    elif selection == 1:
        config = get_db_config_from_env()
        perform_db_dump(config)
    else:
        print("👋 Exiting. Have a great day!")
        exit()
