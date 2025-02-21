import json
import subprocess
import sys
import os
import argparse
from datetime import datetime
from tqdm import tqdm
from simple_term_menu import TerminalMenu  # Interactive menu

# Function to get database configuration from env.php
def get_db_config_from_env():
    """Run PHP command to get env.php configuration and extract database credentials."""
    try:
        cwd = os.getcwd()
        print("CWD:" + cwd)
        possible_paths = [
            f'{cwd}/app/etc/env.php',
            f'{cwd}/../app/etc/env.php',
            f'{cwd}/../../app/etc/env.php'
        ]
        
        for path in possible_paths:
            command = ['php', '-r', f'echo json_encode(include "{path}");']
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0 and result.stdout != "false":
                config = json.loads(result.stdout)
                db_config = config.get('db', {}).get('connection', {}).get('default', {})
                return {
                    'db_host': db_config.get('host'),
                    'db_user': db_config.get('username'),
                    'db_password': db_config.get('password'),
                    'db_name': db_config.get('dbname'),
                    'ignore_tables': [
                        "log_%", "session", "cron_schedule"
                    ]  # Default ignored tables
                }
        
        print("❌ Could not find env.php configuration.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running PHP command: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON: {e}")
        sys.exit(1)

def list_large_tables(config):
    """Fetch only tables larger than 1MB, ordered by size (MB)."""
    print("\n🔍 Fetching table details (only tables > 1MB)...\n")

    query = f"""
    SELECT 
        table_name, 
        table_rows, 
        ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb
    FROM information_schema.tables
    WHERE table_schema = '{config['db_name']}'
    HAVING size_mb > 1
    ORDER BY size_mb DESC;
    """

    show_tables_cmd = (
        f"mysql -u {config['db_user']} -p{config['db_password']} "
        f"-h {config['db_host']} -D information_schema -e \"{query}\""
    )

    try:
        result = subprocess.run(show_tables_cmd, shell=True, check=True, capture_output=True, text=True)
        lines = result.stdout.splitlines()
        
        print(f"{'Table Name':<40}{'Rows':<15}{'Size (MB)':<10}")
        print("=" * 65)
        
        tables = []
        for line in lines[1:]:  # Skip header row
            parts = line.split("\t")
            if len(parts) == 3:
                table_name, rows, size = parts
                tables.append(table_name)
                print(f"{table_name:<40}{rows:<15}{size:<10}")
        
        print(f"\n✅ Showing {len(tables)} tables larger than 1MB.\n")
        return tables
    except subprocess.CalledProcessError as e:
        print(f"❌ Error fetching table details: {e}")
        sys.exit(1)

def list_all_tables(config):
    """Fetch all tables for the database."""
    query = f"SHOW TABLES;"

    show_tables_cmd = (
        f"mysql -u {config['db_user']} -p'{config['db_password']}' "
        f"-h {config['db_host']} -D {config['db_name']} -e \"{query}\""
    )

    try:
        result = subprocess.run(show_tables_cmd, shell=True, check=True, capture_output=True, text=True)
        tables = result.stdout.splitlines()[1:]  # Skip header row
        if not tables:
            print(f"❌ No tables found in database `{config['db_name']}`.")
            sys.exit(1)
        return tables
    except subprocess.CalledProcessError as e:
        print(f"❌ Error fetching all tables: {e}")
        print("🔹 Check if the database exists and credentials are correct.")
        sys.exit(1)

def perform_db_dump(config):
    """Perform the MySQL database dump with gzip compression and track progress."""
    timestamp = datetime.now().strftime('%Y%m%d')
    dump_filename = f"{config['db_name']}_dump_{timestamp}.sql.gz"

    all_tables = list_all_tables(config)  # Dump all tables
    ignore_params = [f"--ignore-table={config['db_name']}.{table}" for table in config.get("ignore_tables", [])]

    print("\n🚀 Starting database dump... This may take a while.\n")

    # Dumping each table individually to track progress
    with tqdm(total=len(all_tables), desc="Dumping Tables", bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} completed") as progress:
        for table in all_tables:
            print(f"📂 Dumping table: {table}...")

            dump_command = (
                f"mysqldump --single-transaction -u {config['db_user']} -p{config['db_password']} "
                f"-h {config['db_host']} {config['db_name']} --triggers "
                f"--tables {table} {' '.join(ignore_params)} "
                f"| sed -e 's/DEFINER[ ]*=[ ]*[^*]*\*/\*/' | gzip >> {dump_filename}"
            )

            try:
                process = subprocess.run(dump_command, shell=True, stderr=subprocess.PIPE, text=True, check=True)
                progress.update(1)
            except subprocess.CalledProcessError as e:
                print(f"❌ Error dumping table {table}: {e}")

    print(f"\n✅ Database dump successful: {dump_filename}\n")

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
        sys.exit(0)

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
