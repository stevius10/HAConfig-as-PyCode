#!/bin/bash

# Verzeichnis, das du überprüfen möchtest
verzeichnis="/share/Extern/Sicherungen/Pi/"
cd "$verzeichnis" || exit

# Änderungszeit der letzten Datei im Verzeichnis in Sekunden seit der Unix-Epoche
letzte_aenderung=$(stat -c %Y $(ls -t "$verzeichnis" | head -1))

# Aktuelle Zeit in Sekunden seit der Unix-Epoche
aktuelle_zeit=$(date +%s)

# Unterschied in Sekunden zwischen der aktuellen Zeit und der letzten Änderung
unterschied=$((aktuelle_zeit - letzte_aenderung))

# Anzahl der Stunden seit der letzten Änderung
stunden=$((unterschied / 3600))

if (( stunden <= 1 )); then
    echo "eben"
elif (( stunden <= 24 )); then
   echo "vor $(echo $stunden)h"
else
    tage=$((stunden / 24))
    echo "vor $(echo $tage)d"
fi
