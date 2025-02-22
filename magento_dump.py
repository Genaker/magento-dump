import argparse
from menu import execute_command

def main():
    parser = argparse.ArgumentParser(description="Magento Database Tool")
    parser.add_argument("command", nargs="?", help="Command to execute: show-tables, db-dump")
    args = parser.parse_args()

    # Delegate command execution
    execute_command(args.command)

if __name__ == "__main__":
    main()
