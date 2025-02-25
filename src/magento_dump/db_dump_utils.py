import subprocess
import sys
import os
import time
from datetime import datetime
from tqdm import tqdm
from .table_utils import list_large_tables

def list_all_tables(config):
    """Fetch all tables for the database."""
    query = "SHOW TABLES;"
    show_tables_cmd = (
        f"mysql -u {config['db_user']} -p'{config['db_password']}' "
        f"-h {config['db_host']} -D {config['db_name']} -e \"{query}\""
    )

    try:
        result = subprocess.run(show_tables_cmd, shell=True, check=True, capture_output=True, text=True)
        tables = result.stdout.splitlines()[1:]
        if not tables:
            print(f"❌ No tables found in database `{config['db_name']}`.")
            sys.exit(1)
        return tables
    except subprocess.CalledProcessError as e:
        print(f"❌ Error fetching all tables: {e}")
        sys.exit(1)

def perform_db_dump(config):
    """Perform the MySQL database dump with gzip compression and track progress."""
    timestamp = datetime.now().strftime('%Y%m%d')
    dump_dir = 'dmp/'
    os.makedirs(dump_dir, exist_ok=True)
    dump_filename = f"{dump_dir}{config['db_name']}_dump_{timestamp}.sql.gz"

    all_tables = list_all_tables(config)
    ignore_params = [f"--ignore-table={config['db_name']}.{table}" for table in config.get("ignore_tables", [])]

    print("\n🚀 Starting database dump...\n")

    with tqdm(total=len(all_tables), desc="Dumping Tables", bar_format="{l_bar}{bar} {n_fmt}/{total_fmt} completed") as progress:
        for table in all_tables:
            print(f"📂 Dumping table: {table}...")

            dump_command = (
                f"mysqldump --single-transaction -u {config['db_user']} -p{config['db_password']} "
                f"-h {config['db_host']} {config['db_name']} --triggers "
                f"--tables {table} {' '.join(ignore_params)} "
                f"| sed -e \"s/DEFINER[ ]*=[ ]*[^*]*\\*/\\*/\" | gzip >> {dump_filename}"
            )

            try:
                process = subprocess.run(dump_command, shell=True, stderr=subprocess.PIPE, text=True, check=True)
                progress.update(1)
            except subprocess.CalledProcessError as e:
                print(f"❌ Error dumping table {table}: {e}")

    print(f"\n✅ Database dump successful: {dump_filename}\n")
