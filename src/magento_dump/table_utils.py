import subprocess
import sys

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
        for line in lines[1:]:
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
