#!/bin/bash

apk add rsync

backup_path="/share/Extern/Sicherungen/Pi"
current_date=$(date +"%d-%m-%Y")
backup_folder="$backup_path/$current_date"
log_file="$backup_folder/backup-log.txt"

ulimit -n 4096

/usr/bin/find "$backup_path" -mindepth 1 -maxdepth 1 -type d -mtime +7 -delete >> "$log_file" 2>&1 || echo "Fehler beim Löschen alter Backup-Ordner" >> "$log_file"
/usr/bin/find "$backup_path" -type f -mtime +7 -delete >> "$log_file" 2>&1 || echo "Fehler beim Löschen alter Backup-Dateien" >> "$log_file"

if mkdir -p "$backup_folder"; then
    echo "Backup-Ordner erstellt: $backup_folder" >> "$log_file"
else
    echo "Fehler beim Erstellen des Backup-Ordners" >&2
fi

if rsync -av --exclude='.storage/xiaomi_miot' --exclude='/homeassistant/.storage/xiaomi_miot' /config/ "$backup_folder" >> "$log_file" 2>&1; then
    echo "Backup erfolgreich" >> "$log_file"
else
    echo "Fehler beim Erstellen des Backups" >> "$log_file"
fi

cat "$log_file"
exit $?