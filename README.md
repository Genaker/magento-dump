# Magento Database Management Tool
A powerful Python script to list Magento database tables and perform MySQL dumps with filtering and compression.

# Features
✅ Show Table Sizes: Lists only tables larger than 1MB, sorted by size.</br>
✅ Dump Full Database: Dumps all tables, ignoring predefined ones.</br>
✅ Interactive CLI: Select options using an interactive menu.</br>
✅ Progress Tracking: Shows real-time progress during MySQL dump.</br>
✅ Config Auto-Detection: Reads Magento env.php for database settings.</br>
✅ Compression: Dumps are gzip compressed for storage efficiency.</br>

# Installation
1. Clone the Repository

```
git clone https://github.com/yourusername/magento-db-tool.git
cd magento-db-tool
```
2. Install Dependencies

```
pip install tqdm simple-term-menu
```
🔹 Run Interactive CLI
```
python3 magento_db_tool.py
```
🔹 Show Tables Bigger Than 1MB
```
python3 magento_db_tool.py show-tables
```
🔹 Dump Entire Magento Database
```
python3 magento_db_tool.py db-dump
```
📝 Commands Overview
Command	Description
- show-tables	List tables larger than 1MB with row count & size
- db-dump	Dumps all tables with gzip compression
- exit	Close the tool
📦 Example Output
Listing Tables

🔍 Fetching table details (only tables > 1MB)...
```
Table Name                            Rows           Size (MB)  
=================================================================
sales_order                           50000         15.6  
catalog_product_entity                120000        12.3  
customer_entity                        30000         8.4  
```
✅ Showing 3 tables larger than 1MB.
Dumping Database
```
🚀 Starting database dump...
📂 Dumping table: sales_order ...
📂 Dumping table: catalog_product_entity ...
📂 Dumping table: customer_entity ...

✅ Database dump successful: magento_luma_dump_20240219.sql.gz
```
🔧 Configuration
This tool automatically extracts your Magento database settings from app/etc/env.php. No manual setup required!

Change ignored tables in ignore_tables inside the script.
⏱ Automate with CRON
To schedule daily database backups at midnight, add this to crontab -e:

```
0 0 * * * /usr/bin/python3 /path/to/magento_db_tool.py db-dump
```

## Deploy to PyPI, follow these steps:

1️. Install Twine (if not installed)
```
pip install twine
```

2️. Build the Package
Inside your project root (magento-dump/):

```
pip install --upgrade setuptools
python setup.py sdist bdist_wheel
```

3️. Upload to PyPI
```
twine upload dist/*
```
This will ask for your PyPI credentials. Once uploaded, you can install your package with:

```
pip install magento-dump
```

📜 License
MIT License. Free to use and modify.
