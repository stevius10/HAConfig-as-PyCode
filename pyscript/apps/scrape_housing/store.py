import aiofiles
import aiofiles.os
import csv
import os
from datetime import datetime

from scrape_housing.apartment import apartment_compare
from generic import IORetriesExceededException

from constants.config import CFG_PATH_DIR_PY_LOGS_DATA, CFG_FILE_SETTINGS_IO_RETRY

def store_path():
    path = f"{CFG_PATH_DIR_PY_LOGS_DATA}/scrape_housings/{datetime.now().strftime("%Y")}-{datetime.now().strftime("%m")}"
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    return f"{path}/{datetime.now().strftime("%d")}-{datetime.now().strftime("%m")}-{datetime.now().strftime("%Y")[-2:]}.csv"

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
    result = existing_filtered.copy()
    for apt in new_filtered:
        if apt:
            found = False
            for e in result:
                if apartment_compare(apt, e):
                    e["last_time"] = datetime.now().strftime("%H:%M")  # Update time
                    found = True
                    break
            if not found:
                apt["first_time"] = datetime.now().strftime("%H:%M")
                apt["last_time"] = datetime.now().strftime("%H:%M")
                result.append(apt)
    return result

# Utilities

async def file_read(file):
    if not aiofiles.os.path.exists(file):
        return []
    exception = None
    for _ in range(CFG_FILE_SETTINGS_IO_RETRY):
        try:
            async with aiofiles.open(file, mode="r", encoding="utf-8") as f:
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
            exception = e
    if exception:
        raise IORetriesExceededException(exception, file)

async def file_write(file, data):
    exception = None
    for _ in range(CFG_FILE_SETTINGS_IO_RETRY):
        try:
            async with aiofiles.open(file, mode="w", encoding="utf-8", newline="") as f:
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
            exception = e
    if exception:
        raise IORetriesExceededException(exception, file)