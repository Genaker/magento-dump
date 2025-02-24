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

    # ✅ Corrected tar command with verbose option
    dump_command = f"tar -czvf {backup_filename} {' '.join(exclude_paths)} ."

    print("\n🚀 Starting Magento Code Dump...\n")

    try:
        subprocess.run(dump_command, shell=True, check=True)
        print(f"\n✅ Magento code successfully archived: {backup_filename}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while dumping Magento code: {e}")

def dump_magento_media():
    """Create a compressed tar.gz archive of the Magento media folder, excluding cache directories."""
    timestamp = datetime.now().strftime('%Y-%m-%d')
    user = os.getenv("USER", "magento-user")
    backup_dir = "dmp/magento-media-backups"
    backup_filename = f"{backup_dir}/{timestamp}_{user}_media.tar.gz"

    # Ensure backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    exclude_paths = [
        "--exclude=pub/media/catalog/cache/*",
        "--exclude=pub/media/tmp/*",
        "--exclude=pub/media/backup/*",
        "--exclude=pub/media/import/*",
        "--exclude=pub/media/captcha/*",
        "--exclude=pub/media/catalog/product/cache/*",
        "--exclude=pub/media/catalog/category/cache/*"
        
    ]

    # ✅ Corrected tar command with verbose option
    dump_command = f"tar -czvf {backup_filename} {' '.join(exclude_paths)} pub/media"

    print("\n🚀 Starting Magento Media Dump...\n")

    try:
        subprocess.run(dump_command, shell=True, check=True)
        print(f"\n✅ Magento media successfully archived: {backup_filename}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while dumping Magento media: {e}")
