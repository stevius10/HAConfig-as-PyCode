#!/bin/bash

# /usr/bin/truncate /config/home-assistant.log -s 0

LOG_FILE="/config/home-assistant.log"
TEMP_FILE="/config/home-assistant.tmp"

rm "$TEMP_FILE"
tail -n 10 "$LOG_FILE" > "$TEMP_FILE"

rm "$LOG_FILE"
cp "$TEMP_FILE" "$LOG_FILE"

current_time=$(date)
echo "Script executed at: $current_time" >> cmd_clear-log.log