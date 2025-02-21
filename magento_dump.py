import argparse
from db_config import get_db_config_from_env
from table_utils import list_large_tables
from dump_utils import perform_db_dump
from menu import show_commands

def main():
    parser = argparse.ArgumentParser(description="Magento Database Tool")
    parser.add_argument("command", nargs="?", help="Command to execute: show-tables, db-dump")
    args = parser.parse_args()

    if args.command == "show-tables":
        config = get_db_config_from_env()
        list_large_tables(config)
    elif args.command == "db-dump":
        config = get_db_config_from_env()
        perform_db_dump(config)
    else:
        show_commands()

if __name__ == "__main__":
    main()
