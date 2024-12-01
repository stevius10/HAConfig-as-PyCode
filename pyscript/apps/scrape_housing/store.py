import csv
import os
import aiofiles

from datetime import datetime

from scrape_housing.apartment import apartment_compare, apartment_update
from generic import IORetriesExceededException

from constants.config import CFG_PATH_DIR_PY_LOGS_DATA, CFG_FILE_SETTINGS_IO_RETRY

# Initialization

def store_dir_create(path):
    """Ensure the directory exists."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def store_path():
    """Generate and ensure the file path."""
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")
    day = datetime.now().strftime("%d")
    path = f"{CFG_PATH_DIR_PY_LOGS_DATA}/scrape_housings/{year}-{month}"
    store_dir_create(path)
    return f"{path}/{day}-{month}-{year[-2:]}.csv"

# Logic

def process(apartments):
    """Process apartments and update the data file."""
    if not isinstance(apartments, list):
        raise TypeError("Expected a list of apartments")
    apartments = flatten_list(apartments)  # Flatten nested lists
    file = store_path()  # Correctly call the sync function
    existing = file_read(file) or []  # Ensure `existing` is a list
    updated = merge(existing, apartments)
    if updated:
        file_write(file, updated)

def flatten_list(nested_list):
    """Flattens a nested list into a single list."""
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list

def merge(existing, new):
    """Merge new apartments into the existing list."""
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
                    apartment_update(e)
                    found = True
                    break
            if not found:
                result.append(apt)
    return result

async def store_file(apartments):
    """Public function to store apartments."""
    process(apartments)

# Utilities

async def file_read(file):
    """Read data from the file."""
    if not os.path.exists(file):
        # Return empty list if the file does not exist
        return []
    exception = None
    for _ in range(CFG_FILE_SETTINGS_IO_RETRY):
        try:
            async with aiofiles.open(file, mode="r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():  # Check if file is empty
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
    """Write data to the file."""
    if not data or not isinstance(data, list):
        raise TypeError("Data must be a list of dictionaries")
    for d in data:
        if not isinstance(d, dict):
            raise TypeError("All items in data must be dictionaries")

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
                        row_values.append(str(row.get(field, "")))
                    row_line = ",".join(row_values) + "\n"
                    f.write(row_line)
            return
        except Exception as e:
            exception = e
    if exception:
        raise IORetriesExceededException(exception, file)
