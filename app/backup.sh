
BACKUP_DIR="./backup"

DB_USER="postgres"

DB_NAME="bot"

mkdir -p $BACKUP_DIR

BACKUP_FILE="${BACKUP_DIR}/$(date +'%Y-%m-%d_%H-%M-%S')_backup.sql"

sudo docker exec app-db-1 pg_dump -U $DB_USER $DB_NAME > $BACKUP_FILE

MAX_BACKUPS=14

if [ "$(ls -1 $BACKUP_DIR | wc -l)" -gt "$MAX_BACKUPS" ]; then
    echo "Удаляем старые резервные копии..."
    ls -1t $BACKUP_DIR | tail -n +$(($MAX_BACKUPS + 1)) | xargs -I {} rm "$BACKUP_DIR/{}"
fi
