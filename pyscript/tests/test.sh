#!/bin/bash

# Navigiere zum Verzeichnis pyscript/tests
cd /homeassistant/pyscript/tests

# Setze das aktuelle Verzeichnis und alle Unterverzeichnisse in den Python-Pfad
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Führe alle Tests rekursiv aus und schreibe das Ergebnis in tests.txt
cd unit
python3 -m unittest discover -s . -p "*.py" > tests.txt