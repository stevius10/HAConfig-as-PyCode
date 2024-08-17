#!/bin/bash

folder="/share/Extern/Sicherungen/Pi/"
cd "$folder" || exit

last_change=$(stat -c %Y "$(ls -t | head -1)")
current_time=$(date +%s)
diff=$((current_time - last_change))
hours=$((diff / 3600))

if (( hours <= 1 )); then
    echo "eben"
elif (( hours <= 24 )); then
   echo "vor $(echo $hours)h"
else
    days=$((hours / 24))
    echo "vor $(echo $days)d"
fi