import json
import subprocess
import os
import sys

def get_db_config_from_env():
    """Run PHP command to get env.php configuration and extract database credentials."""
    try:
        cwd = os.getcwd()
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
                    'ignore_tables': ["log_%", "session", "cron_schedule"]
                }
        
        print("❌ Could not find env.php configuration.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running PHP command: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON: {e}")
        sys.exit(1)
