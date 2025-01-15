import csv
import os
from datetime import datetime

from scrape_housing.apartment import apartment_compare

from constants.config import CFG_PATH_DIR_PY_LOGS_DATA, CFG_FILE_SETTINGS_IO_RETRY

from utils import *


def store_path():
    path = f"{CFG_PATH_DIR_PY_LOGS_DATA}/scrape_housings/{datetime.now().strftime('%Y')}-{datetime.now().strftime('%m')}"
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    return f"{path}/{datetime.now().strftime('%d')}-{datetime.now().strftime('%m')}-{datetime.now().strftime('%Y')[-2:]}.csv"


def store_apartments(apartments):
    if not isinstance(apartments, list):
        raise TypeError("Expected a list of apartments")
    apartments = flatten_list(apartments)
    file = store_path()
    existing = file_read(file) or []
    updated = merge(existing, apartments)
    if updated:
        file_write(file, updated)


def flatten_list(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list

def merge(existing, new):
    if not isinstance(existing, list):
        raise TypeError("Existing data must be a list")
    
    existing_filtered = [e for e in existing if isinstance(e, dict)]
    new_filtered = [n for n in new if isinstance(n, dict)]
    
    result = {e["address"]: e for e in existing_filtered}  # Schlüssel: Adresse
    for apt in new_filtered:
        key = apt.get("address")
        if not key:
            continue
        
        now_time = datetime.now().strftime("%H:%M")
        if key in result:
            result[key]["last_time"] = now_time
        else:
            apt["first_time"] = now_time
            apt["last_time"] = now_time
            result[key] = apt
    
    return list(result.values())

@pyscript_executor
def file_read(file):
    if not os.path.exists(file):
        return []
    exception = None
    for _ in range(CFG_FILE_SETTINGS_IO_RETRY):
        try:
            with open(file, encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    return []
                reader = csv.DictReader(content.splitlines())
                result = []
                for row in reader:
                    if isinstance(row, dict):
                        result.append(row)
                return result
        except Exception as e:
            raise e


@pyscript_executor
def file_write(file, data):
    for _ in range(CFG_FILE_SETTINGS_IO_RETRY):
        try:
            for row in data:
                for key, value in row.items():
                    if value is None:
                        row[key] = ""
            with open(file, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                header_row = ",".join(writer.fieldnames) + "\n"
                f.write(header_row)
                for row in data:
                    row_values = []
                    for field in writer.fieldnames:
                        value = row.get(field, "")
                        row_values.append(str(value))
                    row_line = ",".join(row_values) + "\n"
                    f.write(row_line)
            return
        except Exception as e:
            raise e