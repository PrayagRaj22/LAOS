from dotenv import load_dotenv
import os

load_dotenv() # Reads .env file into environment variables

# -- Server --
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# -- Database --
DB_PATH = os.getenv("DB_PATH", "data/laos.db")

# -- Collection Interval --
COLLECTION_INTERVAL = int(os.getenv("COLLECTION_INTERVAL", 5)) # in seconds

# -- Alert Thresholds --

CPU_ALERT_THRESHOLD = float(os.getenv("CPU_ALERT_THRESHOLD", 85.0)) # in percentage
RAM_ALERT_THRESHOLD = float(os.getenv("RAM_ALERT_THRESHOLD", 85.0)) # in percentage
DISK_ALERT_THRESHOLD = float(os.getenv("DISK_ALERT_THRESHOLD", 90.0)) # in percentage

# -- Notification --
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
ALERT_EMAIL = os.getenv("ALERT_EMAIL", "")

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK", "")

# -- Backup --
BACKUP_SOURCE_DIRS = ["/etc", "/var/www"]
BACKUP_DEST_DIR = os.getenv("BACKUP_DEST_DIR", "data/backups")
BACKUP_KEEP_DAYS = int(os.getenv("BACKUP_KEEP_DAYS", 7)) 