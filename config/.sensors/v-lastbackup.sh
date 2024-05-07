#!/bin/bash

verzeichnis="/share/Extern/Sicherungen/Pi/"
cd "$verzeichnis" || exit

letzte_aenderung=$(stat -c %Y $(ls -t "$verzeichnis" | head -1))

aktuelle_zeit=$(date +%s)

unterschied=$((aktuelle_zeit - letzte_aenderung))

stunden=$((unterschied / 3600))

if (( stunden <= 1 )); then
    echo "eben"
elif (( stunden <= 24 )); then
   echo "vor $(echo $stunden)h"
else
    tage=$((stunden / 24))
    echo "vor $(echo $tage)d"
fi
