import subprocess
import os
from datetime import datetime

def dump_magento_code():
    """Create a compressed tar.gz archive of the Magento codebase, excluding media and cache folders."""
    timestamp = datetime.now().strftime('%Y-%m-%d')
    user = os.getenv("USER", "magento-user")
    backup_dir = "dmp/magento-code-backups"
    backup_filename = f"{backup_dir}/{timestamp}_{user}.tar.gz"

    # Ensure backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    exclude_paths = [
        "--exclude=pub/media/catalog/*",
        "--exclude=pub/media/*",
        "--exclude=dmp/*",
        "--exclude=generated/*",
        "--exclude=nodejs_image_server/*",
        "--exclude=node_modules/*",
        "--exclude=pub/media/backup/*",
        "--exclude=pub/media/import/*",
        "--exclude=pub/media/tmp/*",
        "--exclude=pub/static/*",
        "--exclude=var/*",
        "--exclude=vendor/*",
        "--exclude=venv/*",
        "--exclude=private",
        "--exclude=tests"
    ]

    # ✅ Corrected tar command (Options first, then source directory)
    dump_command = f"tar -czf {backup_filename} {' '.join(exclude_paths)} ."

    print("\n🚀 Starting Magento Code Dump...\n")

    try:
        subprocess.run(dump_command, shell=True, check=True)
        print(f"\n✅ Magento code successfully archived: {backup_filename}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while dumping Magento code: {e}")
